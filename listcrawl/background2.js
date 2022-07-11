var start_url = "http://127.0.0.1:8000/product/get_start_url/"
var add_url = "http://127.0.0.1:8000/product/add_url/"

let listRequest = {
    state: ['token_list'],  // 默认三个令牌 最多可并发发送三次请求
    queue: [],   // 请求队列
    waitqueue: [],  //  等待队列
    // 获取令牌
    getToken: function() {
        return this.state.splice(0, 1)[0];
    },
    // 归还令牌
    backToken: function(token) {
        this.state.push(token);
    },
    // 请求队列
    pushQueue: function(request_obj, type = "first") {
        type == "second" && (this.queue = []); // 每次push新请求的时候  队列清空
        if( this.state.length > 0) {  // 看是否有令牌
            var token = this.getToken();  // 取令牌
            request_obj.token = token;
            this.queue.push(request_obj);
        } else {   // 否则推入等待队列
            this.waitqueue.push(request_obj)
        }
    },
    // 开始执行
    start: function() {
        for(let item of this.queue) {
            if (stop_flag == true){
               console.log("正在采集：",item.url);
               item.request(item.url).then(res => {
                    var jqueryObj = $(res);
                    var rets = jqueryObj.find("#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div")
                    var asins = [];
                    for(var i = 0; i <= rets.length; i++){
                        var asin = $(rets[i]).attr("data-asin");
                        if(asin != "" && asin != undefined){
                            var review_counts = $(rets[i]).find("span.a-size-base.s-underline-text").text();
                            var price = $(rets[i]).find("div.a-row.a-size-base.a-color-base > a > span:nth-child(1) > span.a-offscreen").text();
                            //console.log(asin,review_counts,price);
                            var detail_url_obj = {
                                'url':"https://www.amazon.com/dp/"+asin,
                                'type':'detail_url',
                                'asin':asin,
                                'price':price,
                                'review_counts':review_counts,
                            }
                            console.log("review_counts结果 ：",parseInt(review_counts) < min_review_counts,parseInt(review_counts),min_review_counts);
                            if(parseInt(review_counts) < min_review_counts){ //review数设置
                                 asins.push(asin);
                            }
                        }

                    }

                    res = null;

                    if(asins.length > 0){

                        let options = {
                                method: 'POST',//post请求
                                headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({//post请求参数
                                    url_type:'asin',
                                    urls: asins.join("|"),
                                })
                        }
                        fetch(add_url,options).then(
                        response => response.json()
                        ).then(
                            res=>console.log(res)
                        );
                    }


                    this.backToken(item.token); // 令牌归还

                });

        }
    }

    }
}


function callback(res){
    msg = res.msg;
    if (msg == 1){
        console.log(res.start_url,res.start_page,res.end_page)

        for (var page = res.start_page; page <= res.end_page; page++  ){
            function f1(url) {
            return new Promise((resolve, reject) => {
                    resolve(fetch(url).then(response => response.text())
                    )
                })
            }

            var request_obj = {
                request:f1,
                url:res.start_url.replace("<page>",page.toString()).replace("<pre_page>",(+page-1).toString()),
            }
            listRequest.pushQueue(request_obj);
        }
        listRequest.start();

    } else {
       console.log("没有获取到初始url");
    }
}
fetch(start_url).then(
    response => response.json()
).then(
    res=>callback(res)
);


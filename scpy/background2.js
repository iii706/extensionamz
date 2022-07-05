
for (var page = page_start; page <= page_end; page++  ){
    //list_url = "https://www.amazon.com/s?i=garden&bbn=1055398&rh=n%3A1055398%2Cp_36%3A1000-3000%2Cp_n_date_first_available_absolute%3A1249053011&dc&fs=true&page=<page>&qid=1656595349&rnid=1249051011&ref=sr_pg_<pre_page>"
    list_url = "https://www.amazon.com/s?i=garden&bbn=1055398&rh=n%3A1055398%2Cp_36%3A1000-3000%2Cp_n_date_first_available_absolute%3A1249053011&dc&fs=true&page=<page>&qid=1656595495&rnid=386465011&ref=sr_pg_<pre_page>"
    //list_url = "https://www.amazon.com/s?k=made+in+usa&i=kitchen&rh=n%3A284507&dc&page="+page.toString()+"&crid=29NW53ZKVYBMP&qid=1652338068&rnid=2941120011&sprefix=made+in+usa%2Caps%2C565&ref=sr_pg_"+(page-1).toString()
    var list_url_obj = {
    'url':list_url.replace("<page>",page.toString()).replace("<pre_page>",(page-1).toString()),
    'type':"list_url"
    };
    list_urls.push(list_url_obj);
}






let detailRequest = {
    state: ['token1','token2','token3','token4','token5'],  // 默认三个令牌 最多可并发发送三次请求
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
    getUrl:function(){
        return this.urls.splice(0,1)[0];
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
               product_url = 'https://www.amazon.com/dp/'+item.asin
               //console.log("等待请示数量：",item.token,this.waitqueue.length,listRequest.waitqueue.length,product_url);
               item.request(product_url).then(res => {
                var jqueryObj = $(res);
                var data = {
                    'title':extract(jqueryObj,Paser.title,"title"),
                    'image':extract(jqueryObj,Paser.image,"image"),
                    'asin':item.asin,
                    'price':extract(jqueryObj,Paser.price,"price"),
                    'desc':extract(jqueryObj,Paser.desc,"desc"),
                };

                //add_log_text(data.image+"---"+data.asin+"--"+data.title.slice(0,20)+"..."+data.price+"---",this.waitqueue.length);
                if(item.asin != undefined && data.desc != undefined && data.desc != ""){

                    post_to_locale(data);
                }

                //post_to_locale(data);
                res = null;
                this.backToken(item.token); // 令牌归还
                //console.log("token_length:",this.state.length);
                if(this.waitqueue.length > 0) {
                    var wait = this.waitqueue.splice(0, 1)[0];
                    this.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                    this.start(); // 重新开始执行队列
                }
                //console.log("token_length:",this.state.length);
                if (this.state.length == 4){
                    this.queue = [];//翻页时需要清空队列
                    if (listRequest.waitqueue.length > 0){
                        console.log("需要采集列表页了");
                        var wait = listRequest.waitqueue.splice(0, 1)[0];
                        listRequest.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                        detail_start_flag = true;
                        listRequest.start(); // 重新开始执行队列
                    }
                }


                });
            } else {
               console.log("异常：",this.state);
            }
        }
    },

}




let listRequest = {
    urls:list_urls,
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
    getUrl:function(){
        return this.urls.splice(0,1)[0];
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
               console.log("正在采集：",detailRequest.waitqueue.length,detail_start_flag,item.url);
               //add_log_text("正在采集："+detailRequest.waitqueue.length.toString()+"---"+detail_start_flag.toString()+'----'+item.url);
               item.request(item.url).then(res => {
                    var jqueryObj = $(res);
                    var rets = jqueryObj.find("#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div")
                    var next_page_detail = [];
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
                            //console.log("review_counts结果 ：",parseInt(review_counts) < min_review_counts,parseInt(review_counts),min_review_counts);
                            if(parseInt(review_counts) < min_review_counts){ //review数设置
                                 next_page_detail.push(detail_url_obj);
                            }
                        }

                    }

                    res = null;
                    //console.log("next_page_detail",next_page_detail);
                    if(next_page_detail.length == 0){ //整页的产品数据都是大于设定的review_counts值的时候
                        detail_start_flag = true;
                    }
                    for (var j = 0; j < next_page_detail.length; j++){
                            function f1(url) {
                            return new Promise((resolve, reject) => {
                                resolve(ajax_get(url))
                                })
                            }
                            var request_obj = {
                                request:f1,
                                asin:next_page_detail[j].asin
                            }
                            detailRequest.pushQueue(request_obj);
                        }
                    next_page_detail = null;
                    if(detail_start_flag){
                        detailRequest.start();
                        detail_start_flag = false;
                    }
                    this.backToken(item.token); // 令牌归还

                });

        }
    }

    }
}
function ajax_get(url){
     return $.ajax({
             methon : "get",
             async : true,
             url : url,
             success : function(json){
                 return json
             },
             complete: function (XHR, TS) { XHR = null }
    });
}


for (var i = 0; i < list_urls.length; i++){
    function f1(url) {
    return new Promise((resolve, reject) => {
        resolve(ajax_get(url))
        })
    }
    var request_obj = {
        request:f1,
        url:list_urls[i].url
    }
    listRequest.pushQueue(request_obj);
}
listRequest.start();

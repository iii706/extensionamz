var count = '10'
var get_asin_url = "http://127.0.0.1:8000/product/get_asin_url/?count="+count
var product_content_post_url = "http://127.0.0.1:8000/product/post/"


let detailRequest = {
    state: ['token1','token2','token3','token4'],  // 默认三个令牌 最多可并发发送三次请求
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
               product_url = 'https://www.amazon.com/dp/'+item.asin
               item.request(product_url).then(res => {
                var jqueryObj = $(res);
                var data = {
                    'title':product_extract(jqueryObj,product_Paser.title,"title"),
                    'image':product_extract(jqueryObj,product_Paser.image,"image"),
                    'asin':item.asin,
                    'price':product_extract(jqueryObj,product_Paser.price,"price"),
                    'desc':product_extract(jqueryObj,product_Paser.desc,"desc"),
                };

                console.log("price",data.price);
                var seller_url = product_extract(jqueryObj,product_Paser.seller_url,"seller_url");
                data['seller_id'] = "";
                if(seller_url != "" && seller_url != undefined) {
                    if (seller_url.indexOf("seller=") != -1){
                        data['seller_id'] = seller_url.split("seller=")[1].split("&")[0]
                    }
                }
                console.log("卖家链接是：",data,item.asin != undefined && data.desc != undefined && data.desc != "" && data.seller_id != "");
                if(item.asin != undefined && data.desc != undefined && data.desc != "" && data.seller_id != ""){
                    data['ret'] = 1;
                } else {
                    data['ret'] = 0;
                }
                let options = {
                                method: 'POST',//post请求
                                headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(data)
                        }
                fetch(product_content_post_url,options).then(
                response => response.json()
                ).then(
                    res=>console.log(res)
                );

                //post_to_locale(data);
                res = null;
                this.backToken(item.token); // 令牌归还

                if(this.waitqueue.length > 0) {
                    var wait = this.waitqueue.splice(0, 1)[0];
                    this.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                    this.start(); // 重新开始执行队列
                }

                if (this.state.length == 4){
                    chrome.runtime.reload();
                }
                }).catch(e => console.log(e));
            }
        }
    },

}

function callback(res){
    msg = res.msg;
    if (msg == 1){
        asins = res.asins;
        console.log(asins)
        for (var i = 0; i < asins.length ; i++  ){
            function f1(url) {
            return new Promise((resolve, reject) => {
                    resolve(fetch(url).then(response => response.text())
                    )
                })
            }
            var request_obj = {
                request:f1,
                asin:asins[i],
                //asin:'B0B3MK69B3',
            }
            detailRequest.pushQueue(request_obj);
        }
        detailRequest.start();

    } else {
       console.log("没有获取到需要抓取的产品链接");
    }
}
fetch(get_asin_url).then(
    response => response.json()
).then(
    res=>callback(res)
);








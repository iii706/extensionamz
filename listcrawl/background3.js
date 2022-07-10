function post_to_locale(data){
        $.ajax({
            async : true,
            url : "http://127.0.0.1:8000/product/post",
            type : "GET",
            dataType : "jsonp", // 返回的数据类型，设置为JSONP方式
            jsonp : 'callback', //指定一个查询参数名称来覆盖默认的 jsonp 回调参数名 callback
            jsonpCallback: 'handleResponse', //设置回调函数名
            data : data,
            success: function(response, status, xhr){
                XHR = null
            },
            complete: function (XHR, TS) { XHR = null }
            });
}

    let detail_start_flag = true;
    let stop_flag = true;
    let asin = $("#asin").val();
    let page_start = 1;
    let page_end = 50;
    let list_url = "";
    let list_urls = [];


    for (var page = page_start; page <= page_end; page++  ){
        list_url = "https://www.amazon.com/s?k=made+in+usa&i=kitchen&rh=n%3A284507&dc&page="+page.toString()+"&crid=29NW53ZKVYBMP&qid=1652338068&rnid=2941120011&sprefix=made+in+usa%2Caps%2C565&ref=sr_pg_"+(page-1).toString()
        let list_url_obj = {
        }
        list_url_obj['url'] = list_url;
        list_url_obj['type'] = "list_url";
        list_urls.push(list_url_obj);
    }


    let detail_urls = [];

    add_log_text("开始执行。。。",list_urls.length);
    //console.log(list_urls);

let detailRequest = {
    urls:detail_urls,
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
    getUrl:function(){
        return this.urls.splice(0,1)[0];
    },
    // 请求队列
    pushQueue: function(args, type = "first") {
        type == "second" && (this.queue = []); // 每次push新请求的时候  队列清空
        for(var i = 0; i < args.length; i++) {
            if( this.state.length > 0) {  // 看是否有令牌
                var token = this.getToken();  // 取令牌
                var obj = {
                    token,
                    request: args[i],
                }
                this.queue.push(obj);
            } else {   // 否则推入等待队列
                this.waitqueue.push(args[i])
            }
        }
    },
    // 开始执行
    start: function() {
        for(let item of this.queue) {
            let url_item = this.getUrl()
            if (url_item != undefined && url_item.type == "detail_url" && stop_flag == true){
               item.request(url_item['url']).then(res => {
                var jqueryObj = $(res);
                var data = {
                    'title':extract(jqueryObj,Paser.title,"title"),
                    'image':extract(jqueryObj,Paser.image,"image"),
                    'asin':url_item.asin,
                    'price':extract(jqueryObj,Paser.price,"price"),
                    'desc':extract(jqueryObj,Paser.desc,"desc"),
                }
                //console.log(data);
                if(url_item.asin != undefined){
                    //add_log_text(data.image+"---"+data.asin+"--"+data.title.slice(0,20)+"..."+data.price+"---",this.waitqueue.length);
                    post_to_locale(data);
                }

                //post_to_locale(data);
                res = null;
                this.backToken(item.token); // 令牌归还
                if(this.waitqueue.length > 0) {
                    var wait = this.waitqueue.splice(0, 1);
                    this.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                    this.start(); // 重新开始执行队列
                }
                });
            } else {
               this.waitqueue = [];
            }





        }
    },

}



let listRequest = {
    urls:list_urls,
    state: ['token1'],  // 默认三个令牌 最多可并发发送三次请求
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
    pushQueue: function(args, type = "first") {
        type == "second" && (this.queue = []); // 每次push新请求的时候  队列清空
        for(var i = 0; i < args.length; i++) {
            if( this.state.length > 0) {  // 看是否有令牌
                var token = this.getToken();  // 取令牌
                var obj = {
                    token,
                    request: args[i]
                }
                this.queue.push(obj);
            } else {   // 否则推入等待队列
                this.waitqueue.push(args[i])
            }
        }
    },
    // 开始执行
    start: function() {
        for(let item of this.queue) {
            let url_item = this.getUrl()
            if (url_item != undefined && stop_flag == true){
               item.request(url_item.url).then(res => {
                    var jqueryObj = $(res);
                    var rets = jqueryObj.find("#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div")
                    for(var i = 0; i <= rets.length; i++){
                        asin = $(rets[i]).attr("data-asin");
                        if(asin){
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
                            detail_urls.push(detail_url_obj);
                        }

                    }
                    //add_log_text(detail_urls.length);


                    res = null;

                    //console.log(detail_urls);
                    for (var j = 0; j <= detail_urls.length; j++){
                            function f1(url) {
                            return new Promise((resolve, reject) => {
                                resolve(ajax_get(url))
                                })
                            }
                            detailRequest.pushQueue([f1]);
                        }

                    if(detail_start_flag){

                        detailRequest.start();
                        detail_start_flag = false;
                    }

                    //post_to_locale(data);
                    this.backToken(item.token); // 令牌归还
                    if(this.waitqueue.length > 0) {
                        var wait = this.waitqueue.splice(0, 1);
                        this.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                        this.start(); // 重新开始执行队列
                    }


                });
            } else {
             this.waitqueue = [];
            }
        }
    },

}
function ajax_get(url){
     return $.ajax({
             methon : "get",
             async : true,
             url : url, //跨域请求的URL
             success : function(json){
                 return json
             },
             complete: function (XHR, TS) { XHR = null }
    });
}


for (var i = 0; i <= list_urls.length; i++){
    function f1(url) {
    return new Promise((resolve, reject) => {
        resolve(ajax_get(url))
        })
    }
    listRequest.pushQueue([f1]);
}
listRequest.start();


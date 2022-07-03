$(document).ready(function(){
  $("#stop").click(function(){
    alert("真的停止么？");
    stop_flag = false;
    add_log_text("停止采集");
  });

  $("#start").click(function(){



    for (var page = page_start; page <= page_end; page++  ){
        //list_url = "https://www.amazon.com/s?i=garden&bbn=1055398&rh=n%3A1055398%2Cp_36%3A1000-3000%2Cp_n_date_first_available_absolute%3A1249053011&dc&fs=true&page=<page>&qid=1656595349&rnid=1249051011&ref=sr_pg_<pre_page>"
        list_url = "https://www.amazon.com/s?i=garden&bbn=1055398&rh=n%3A1055398%2Cp_36%3A1000-3000%2Cp_n_date_first_available_absolute%3A1249053011&dc&fs=true&page=<page>&qid=1656595495&rnid=386465011&ref=sr_pg_<pre_page>"
        //list_url = "https://www.amazon.com/s?k=made+in+usa&i=kitchen&rh=n%3A284507&dc&page="+page.toString()+"&crid=29NW53ZKVYBMP&qid=1652338068&rnid=2941120011&sprefix=made+in+usa%2Caps%2C565&ref=sr_pg_"+(page-1).toString()
        let list_url_obj = {
        }
        list_url_obj['url'] = list_url.replace("<page>",page.toString()).replace("<pre_page>",(page-1).toString());
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
                console.log("等待请示数量：",this.waitqueue.length,listRequest.waitqueue.length,url_item.url);

               item.request(url_item['url']).then(res => {
                var jqueryObj = $(res);
                var data = {
                    'title':extract(jqueryObj,Paser.title,"title"),
                    'image':extract(jqueryObj,Paser.image,"image"),
                    'asin':url_item.asin,
                    'price':extract(jqueryObj,Paser.price,"price"),
                    'desc':extract(jqueryObj,Paser.desc,"desc"),
                };

                //add_log_text(data.image+"---"+data.asin+"--"+data.title.slice(0,20)+"..."+data.price+"---",this.waitqueue.length);
                if(url_item.asin != undefined && data.desc != undefined && data.desc != ""){
                    //console.log(data);
                    //add_log_text(data.image+"---"+data.asin+"--"+data.title.slice(0,20)+"..."+data.price+"---",this.waitqueue.length);
                    //console.log("保存到数据库");
                    //console.log(data)
                    post_to_locale(data);
                }

                //post_to_locale(data);
                res = null;
                this.backToken(item.token); // 令牌归还
                console.log("执行12421：",this.waitqueue.length,this.waitqueue);
                if(this.waitqueue.length > 0) {
                    var wait = this.waitqueue.splice(0, 1);
                    this.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                    this.start(); // 重新开始执行队列
                } else {
                    console.log("执行12422：",this.waitqueue.length,this.waitqueue);
                    if(listRequest.waitqueue.length > 0) {
                        var wait = listRequest.waitqueue.splice(0, 1);
                        listRequest.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                        listRequest.start(); // 重新开始执行队列
                    }

                }


                });
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
               console.log("正在采集：",detailRequest.waitqueue.length,detail_start_flag,url_item.url);
               if(detailRequest.waitqueue.length == 0){
                   detail_start_flag = true; //防止等待队列没有数据停止。
               }
               item.request(url_item.url).then(res => {
                    var jqueryObj = $(res);
                    var rets = jqueryObj.find("#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div")
                    var next_page_detail = [];
                    for(var i = 0; i <= rets.length; i++){
                        var asin = $(rets[i]).attr("data-asin");
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
                            if(parseInt(review_counts) < min_review_counts){ //review数设置
                                 detail_urls.push(detail_url_obj);
                                 next_page_detail.push(detail_url_obj);
                            }
                        }

                    }
                    //add_log_text(detail_urls.length);


                    res = null;

                    //console.log(detail_urls);
                    for (var j = 0; j <= next_page_detail.length; j++){
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
                    if(detailRequest.waitqueue.length < 10 && this.waitqueue.length > 0) {
                        var wait = listRequest.waitqueue.splice(0, 1);
                        listRequest.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                    }
                    listRequest.start(); // 重新开始执行队列
                });
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
  });
});
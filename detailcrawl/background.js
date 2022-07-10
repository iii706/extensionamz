$(document).ready(function(){
  $("#start").click(function(){
    var asin = $("#asin").val();
    let list_url = "https://www.amazon.com/s?k=made+in+usa&i=kitchen&rh=n%3A284507&dc&page=7&crid=29NW53ZKVYBMP&qid=1652338068&rnid=2941120011&sprefix=made+in+usa%2Caps%2C565&ref=sr_pg_6"
    let url_obj = {
        'url':list_url,
        'url_type':'list_url'
    }
    //alert(asin);
    var urls = [
    //'https://www.amazon.com/dp/B08RS5FBCW/',
    //'https://www.amazon.com/dp/B08NDPLRST/',
    //'https://www.amazon.com/dp/B09LM56LJ3/',
    //'https://www.amazon.com/dp/B09V6YYQ2J/',
    //'https://www.amazon.com/dp/B09Z2Q6NH2/',
    //'https://www.amazon.com/dp/B09LM56LJ3/',
    //'https://www.amazon.com/dp/B09Z2DWY1S/',
    ];
    var asins = [
        //'B08RS5FBCW',
        //'B08NDPLRST',
        //'B09LM56LJ3',
        //'B09V6YYQ2J',
        //'B09Z2Q6NH2',
        //'B09LM56LJ3',
        //'B09Z2DWY1S',
    ];
    // if (asin != ""){
    // urls.push("https://www.amazon.com/dp/"+asin);
    // asins.push(asin);
    // }
    // 
    urls.push(url_obj)
   


add_log_text("开始执行。。。");

let tokensRequest = {
    urls:urls,
    asins:asins,
    rets_arr : [],
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
    getAsin:function(){
         return this.asins.splice(0,1)[0];
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
                    asin:this.getAsin(),
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
            let list_url_item = this.getUrl()
            if (list_url_item != undefined && list_url_item['url_type'] == "list_url"){
                //console.log("列表的网页");
                //console.log(list_url_item['url']);
                item.request(list_url_item['url']).then(res => {
                    var jqueryObj = $(res);

                    var rets = jqueryObj.find("#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div")
                    for(var i = 0; i <= rets.length; i++){
                        asin = $(rets[i]).attr("data-asin");
                        if(asin){
                            review_counts = $(rets[i]).find("span.a-size-base.s-underline-text").text();
                            price = $(rets[i]).find("div.a-row.a-size-base.a-color-base > a > span:nth-child(1) > span.a-offscreen").text();
                            console.log(asin,review_counts,price);

                            url_obj = {
                                'url':"https://www.amazon.com/dp/"+asin,
                                'url_type':'asin_url'
                            }


                            urls.push(url_obj);

                        }
                        
                    }

                    console.log(urls);
                    for (var i = 0; i <= urls.length; i++){
                            function f1(url) {
                            return new Promise((resolve, reject) => {
                                resolve(ajax_get(url))
                                })
                            }
                            this.pushQueue([f1]);
                        }
                    this.start();
    
                    var data = {
                        
                    }
                });




            } else {

                   

                    if (list_url_item != undefined && list_url_item['url_type'] == "asin_url"){
                       item.request(list_url_item['url']).then(res => {
                        var jqueryObj = $(res);
                        var data = {
                            'title':extract(jqueryObj,Paser.title,"title"),
                            'image':extract(jqueryObj,Paser.image,"image"),
                            'asin':item.asin,
                            'price':extract(jqueryObj,Paser.price,"price"),
                            'desc':extract(jqueryObj,Paser.desc,"desc"),
                        }
                        if(item.asin != undefined){
                            add_log_text(data.image+"---"+item.asin+"--"+data.title.slice(0,50)+"..."+data.price+"---"+data.rating+"---"+data.rankandtext);
                            post_to_locale(data);
                        }
                        
                        post_to_locale(data);
                        this.backToken(item.token); // 令牌归还
                        if(this.waitqueue.length > 0) {
                            var wait = this.waitqueue.splice(0, 1);
                            this.pushQueue(wait, "second"); // 从等待队列进去的话 就是第二中的push情况了
                            this.start(); // 重新开始执行队列
                        }

                        }); 
                    }

                    
                }

            
        }
    },

}
function ajax_get(url){
     return $.ajax({
             methon : "get",
             url : url, //跨域请求的URL
             success : function(json){
                 return json
             }
    });
}
for (var i = 0; i <= urls.length; i++){
    function f1(url) {
    return new Promise((resolve, reject) => {
        resolve(ajax_get(url))
    })
    }
    tokensRequest.pushQueue([f1]);
}


tokensRequest.start();

  });
});
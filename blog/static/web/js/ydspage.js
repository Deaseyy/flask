
// 分页
$(function (){
            //  给page节点添加点击

            $('#yema a').click(function (e) {
                $(this).addClass('curPage').siblings().removeClass('curPage')
                var index = $(this).index()+1
                get_atc(index)
            })

            // 获取点击对应页的文章
            function get_atc(page){
                var href= location.href
                $.post(href, {'page':page}, function (data) {
                    $('#article').empty()
                    var atcss = data.atcss
                    console.log(atcss)
                    for(var i=0;i<atcss.length;i++) {
                        var id = atcss[i].id
                        var title = atcss[i].title
                        var desc = atcss[i].desc
                        var cretime = atcss[i].create_time

                        li = $('<li></li>')
                        $('<i><a href="/web/share/show_atc/' + id +'/"><img src="/static/web/images/2.jpg"></a></i>').appendTo(li)
                        $('<h3><a href="/web/share/show_atc/' + id + '/">' + title+ '</a></h3>').appendTo(li)
                        $('<p>' + desc + '</p>').appendTo(li)
                        li.appendTo('#article')
                    }

                })
            }

        })
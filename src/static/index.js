console.log("this is in index.js");



//一般直接写在一个js文件中
layui.use(['layer', 'form'], function(){
  var layer = layui.layer
  ,form = layui.form;

  layer.msg('Hello World');
});

//上传文件
layui.use('upload', function(){
  var $ = layui.jquery
  ,upload = layui.upload;

  upload.render({
    elem: '#test3'
    ,url: 'http://127.0.0.1:5000/upload_apk' //改成您自己的上传接口
    ,accept: 'file' //普通文件
    ,done: function(res){
      layer.msg('上传成功');
      console.log(res);
    }
  });
});


// //表格
// layui.use('table', function(){
//   var table = layui.table;
//   table.render({
//     elem: '#test'
//     ,height: 312
//     ,url: '/getdata' //数据接口
//     ,page: true //开启分页
//     ,limit: 10
//     ,cols: [[ //表头
//       {field: 'sha1', title: 'sha1', width:200}
//       ,{field: 'pkg', title: '包名', width:200, sort: true}
//       ,{field: 'cert', title: '证书', width:200}
//       ,{field: 'dn', title: 'dn', width: 100, sort: true}
//       ,{field: 'vername', title: '版本', width: 100, sort: true}
//       ,{field: 'appname', title: '应用名称', width: 100}
//       ,{field: 'add_time', title: '记录时间', width: 135, sort: true}
//     ]]
//   });

//     //监听行单击事件
// table.on('row(test)', function(obj){
//   console.log(obj.tr); //得到当前行元素对象
//   console.log(obj.data); //得到当前行数据
//   console.log("this is row");
//   //obj.del(); //删除当前行
//   //obj.update(fields) //修改当前行数据
// });
// });





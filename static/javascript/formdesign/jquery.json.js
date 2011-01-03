//tojson based on http://devers.blogspot.com/2007/09/worlds-smallest-tojson-function.html
(function($) {       
    $.toJSON = function(obj)
    {
       switch (typeof obj) {
        case 'object':
         if (obj) {
          var list = [];
          if (obj instanceof Array) {
           for (var i=0;i < obj.length;i++) {
            list.push($.toJSON(obj[i]));
           }
           return '[' + list.join(',') + ']';
          } else {
           for (var prop in obj) {
            list.push('"' + prop + '":' + $.toJSON(obj[prop]));
           }
           return '{' + list.join(',') + '}';
          }
         } else {
          return 'null';
         }
        case 'string':
         return '"' + obj.replace(/(["'])/g, '\\$1') + '"';
        case 'number':
        case 'boolean':
         return new String(obj);
       }
   } 
})(jQuery);





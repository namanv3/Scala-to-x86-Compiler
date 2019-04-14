class Demo(){
  def quicksort(var x:Array[Int](6)={}, var first:Int, var last:Int):Int={
                var pivot:Int;
                var j:Int;
                var temp:Int;
                var i:Int;
                var f:Int;
                var e:Int;
                var a:Int;

                if(first<last){
                  var pivot=first
                  var i=first
                  var j=last+1

                  while(i<j){
                  while((x[i] <= x[pivot]) && (i <= last)){
                    i= i + 1}
                  while(x[j]>x[pivot]){
                    j= j - 1}
                                if(i<j){
                                        var temp=x[pivot]
                                }
                        }
                        var temp=x[pivot]
                        var f = j - 1
                        var e = j + 1

                  this.quicksort(x,first,f)
                  this.quicksort(x,e,last)

                return 0
                }
return 0;
}
}

// Calculating a Fibonacci sequence recursively using Scala.
object Fibonacci{

    def fib(prevPrev: Int, prev: Int) = {
        val next:Int = prevPrev + prev
        if (next < 100000){
		          next += 1;
	      }
	      else
	      {
	      	return
	      }
        fib(prev, next)
    }

}

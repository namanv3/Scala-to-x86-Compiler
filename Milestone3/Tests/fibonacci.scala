// Calculating a Fibonacci sequence recursively using Scala.
object Fibonacci{

    def fib(prevPrev: Int, prev: Int) = {
        val next:Int = prevPrev + prev
        if (next > 1000000){
		          break;
	      }
        fib(prev, next)
    }

}

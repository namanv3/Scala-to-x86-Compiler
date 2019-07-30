object ackermann {
	def func (m : Int, n : Int) : Int = {
		if (m == 0) return n + 1
		if (n == 0) return func(m-1,1)
		return func(m-1,func(m,n-1))
	}

	def main(args : Array[String]) {
		val m = scala.io.StdIn.readInt()
		val n = scala.io.StdIn.readInt()
		println(func(m,n))
	}
}
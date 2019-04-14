object fibonacci {
	def fib (n : Int) : Int = {
		var a = 0
		var b = 1
		var c = 0
		if (n == 0) return a

		for (i <- 2 to n) {
			c = a + b
			a = b
			b = c
		}
		return b
	}

	def main (args : Array[String]) {
		while (true) {
			val a = scala.io.StdIn.readInt()
			println(fib(a))
		}
	}
}
object matmul {
	def mult (A : Array[Array[Int]], B : Array[Array[Int]]) : Array[Array[Int]] {
		
	}


	def main(args : Array[String]) {
		val m = scala.io.StdIn.readInt()
		val n = scala.io.StdIn.readInt()

		var A = new Array[Array[Int]](m)
		var B = new Array[Array[Int]](n)

		for (i <- 0 to m - 1) {
			A(i) = new Array[Int](n)
			for (j <- 0 to n - 1) A(i)(j) = i ^ j + (i * j) / (j | 0x22) - i
		}

		for (i <- 0 to n - 1) {
			B(i) = new Array[Int](m)
			for (j <- 0 to m - 1) B(i)(j) = i | j * (i - j) / (j ^ 0x22) - j
		}
	}
}
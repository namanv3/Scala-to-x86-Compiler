trait node {
	def value() : Int
	def nextNode() : node
	def push(a : Int)
	def search(a : Int) : Boolean
}

object NilNode extends node {
    override def value() = ???
	override def nextNode() = ???
	override def push(a : Int) = ???
	override def search(a : Int) = ???
}

class linkedList (num : Int, next_ : node) extends node {
	var info = num
	var next = next_

	override def value() : Int = {
		return info
	}

	override def nextNode() : node = {
		return next
	}

	override def push (a : Int) {
		if (this.next == NilNode) {
			val newNode = new linkedList(a, NilNode)
			this.next = newNode
			return
		}
		this.next.push(a)
	}

	override def search (a : Int) : Boolean = {
		if (this.info == a) return true
		if (this.next == NilNode) return false
		return this.next.search(a)
	}
}

object lList {
	def main(args : Array[String]) {
		var a = scala.io.StdIn.readInt()
		val head = new linkedList(a, NilNode)

		while (a != -1) {
			a = scala.io.StdIn.readInt()
			head.push(a)
		}

		val key = scala.io.StdIn.readInt()
		if (head.search(key)) println("found")
		else println("not found")
	}
}
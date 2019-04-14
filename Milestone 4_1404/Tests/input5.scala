object Demo {
   def main(args: Array[String]) = {
		    var myList = Array(1.9, 2.9, 3.4, 3.5)

		    // Print all the array elements
		    for ( x <- myList ) {
		       println( x )
		    }

		    // Summing all elements
		    var total = 0.0;

		    for ( i <- myList) {
		       total += i;
		    }
		    println("Total is " + total);

		    // Finding the largest element
		    var max = myList(0);

		    for ( i <- myList ) {
		       if (i > max)
					 {
						 	max = i;
					}
		    }
		 println("Max is " + max)
   }
}

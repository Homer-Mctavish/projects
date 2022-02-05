// Creating an array using array syntax and explicit type definition Array<String>
var strings:Array<String> = ["Apple", "Pear", "Banana"];
trace(strings);

// Creating an array with float values
// Here, the type definition Array<Float> is left out - it is infered by the compiler
var floats = [10.2, 40.5, 60.3];
trace(floats);

var ints = [for(i in 0...5) i];
trace(ints); // [0,1,2,3,4]

var evens = [for(i in 0...5) i*2];
trace(evens); // [0,2,4,6,8]

var chars = [for(c in 65...70) String.fromCharCode(c)];
trace(chars); // ['A','B','C','D','E']

var x = 1;
var bits = [while(x <= 64) x = x * 2];
trace(bits); // [2,4,8,16,32,64,128]

var strings:Array<String> = [];

// Adds "Hello" at index 0, offsetting elements to the right by one position
strings.insert(0, "Hello");

// Prepends "Haxe" to the start of the array
strings.unshift("Haxe");

// Appends "World" to the end of the array
strings.push("World");

// Appends "foo", "bar" elements to the end of a copy of the array
strings = strings.concat(["foo", "bar"]);

var strings:Array<String> = ["first", "foo", "middle", "foo", "last"];

// Removes first occurence of "middle" in the array
strings.remove("middle");

// Removes and returns three elements beginning with (and including) index 0
var sub = strings.splice(0, 3);

// Removes and returns first element of the array
var first = strings.shift();

// Removes and returns last element of the array
var last = strings.pop();

var strings:Array<String> = ["first", "foo", "middle", "foo", "last"];

// Retrieves first array element
var first = strings[0];

// Retrieves last array element
var last = strings[strings.length - 1];

// Retrieves first occurrence of "foo" string
var first = strings[strings.indexOf("foo")];

// Retrieves last occurrence of "foo" string
var last = strings[strings.lastIndexOf("foo")];

var items = ["a", "b", "c"];
for (item in items) {
    trace(item);
}
// a
// b
// c

var items = ["a", "b", "c"];
for (index => item in items) {
    trace('$index : $item');
}
// 0 : a
// 1 : b
// 2 : c

var strings:Array<String> = ["first", "second", "last"];
var stringsCopy = strings.copy();

stringsCopy.push("best"); // add extra value to the copied list

trace(strings); // ["first", "second", "last"];
trace(stringsCopy); // ["first", "second", "last", "best"];

var fruits:Array<String> = ["apple", "pear", "banana"];
var bananas = fruits.filter(item -> item == "banana");
trace(bananas); // ["banana"]

var fruits:Array<String> = ["apple", "pear", "banana"];
var bananas = [for (v in fruits ) if (v == "banana") v];
trace(bananas); // ["banana"]

var items:Array<String> = ["first", "second", "last"];
var importantItems = items.map(item -> item.toUpperCase());
trace(importantItems); // ["FIRST","SECOND","LAST"]

var items:Array<String> = ["first", "second", "last"];
var importantItems = [for(v in items) v.toUpperCase()];
trace(importantItems); // ["FIRST","SECOND","LAST"]

var items:Array<String> = ["first", "second", "last"];
items.reverse();
trace(items); // ["last","second","first"]

var items:Array<String> = ["first", "second", "last"];
// Returns a string of array elements concatenated by separator string
var joinedItems:String = items.join(" / ");
trace(joinedItems); // "first / second / last"

// Returns a string representation of the array structure
var itemsAsString:String = items.toString();
trace(itemsAsString); // "first,second,last"

// Retrieves the array
var arrayOfInts:Array<Int> = array2d[0];
var arrayOfArrayOfInts:Array<Array<Int>> = array3d[0];
// Retrieves only first element
var first2d = array2d[0][0];
var first3d = array3d[0][0][0];

## introduction 
this page will introduce you some of the Php tips uage and gotchas.

## autoload and namespace/PEAR

well, PHP has a promiscous way of organizing its package and names.

suppose that I have the followign AutoLoad code 

```
<?php 


// Atoload alows you to autoload packages and etc...


// 1) Version one
// function __autoload( $classname ) {
// 	include_once( "$classname.php" );
// }

// 2) version 2

// function __autoload($clasname){ 
// 	$path = str_replace('_', DIRECTORY_SEPARATOR, $classname);
// 	include_once("$path.php"));
// }

// $y = new business_ShopProduct();



// 3) version 3
function __autoload( $classname ) {
	if ( preg_match( '/\\\\/', $classname ) ) {
		$path = str_replace('\\', DIRECTORY_SEPARATOR, $classname );
	} else {
		$path = str_replace('_', DIRECTORY_SEPARATOR, $classname );
	}

	require_once( "$path.php" );
}

// demonstrate the use of PEAR way
$z = new shop_ShopProduct( 'The Darkening', 'Harry', 'Hunter', 12.99 );
$z->print_data();
?>
```

if the our code is organized with the PEAER way, so the shop\ShopProduct should be something like this:


```
<?php

// test class - autolaoding @ see more details from ../Autoloading.php
// shop_ShopProduct demonstrate the strength of the PEAR naming....
// don't know PEAR naming, go google.com

class shop_ShopProduct { 
	public $name;
	public $category;
	public $subcategory;
	public $price;

	function __construct($name, $category, $subcategory, $price) {
		$this->name = $name;
		$this->category = $category;
		$this->subcategory = $subcategory;
		$this->price = $price;
	}

	function print_data() {
		return "{$this->name} {$this->category} {$this->subcategory} {$this->price} ";
	}
}

?>
```

However, if you organize your code with the namespace way, you'd probably do this; 

in Autoload.php do this way of calling.

```
$z = new shop\ShopProduct('The Darkening', 'Harry', 'Hunter', 12.99);
$z->print_data();
```

and you may need to change namespace declaration of ShopProduct.php as follow.
```
namespace shop;
class ShopProduct {
  // ...
}
```

## php does not need to declare instances

well, it is POSSIBLE that you dont' declare an variable before you can use it . here is an example.

```
<?php

// Learn about Methods 
// key here is to use the get_class method to return a string representing the class.
// methods that ca be covered in this situation include the following
//  1) method

// if you add the following namespace above

class CdProduct { 
	// well it is not necessary to declare the variables below, 
	// but we'd recommended that you do this.
	//

	/*
	private $subject;
	private $name;
	private $edition;
	private $discount;
	*/
	function CdProduct($subject, $name, $edition, $price, $discount) { 
		$this->subject= $subject;
		$this->name = $name;
		$this->eidtion = $edition;
		$this->discount = $discount;
	}

	function getTitle() {
		return $this->subject;
	}
}


print_r( get_class_methods('CdProduct'));


// usage : determine if a method exist 
function getProduct() {
	return new CdProduct( "Exile on Coldharbour Lane",
			"The", "Alabama 3", 10.99, 60.33 );
}

$product = getProduct(); // acquire an object
$method = "getTitle"; // define a method name

if ( in_array( $method, get_class_methods( $product ) ) ) {
	print $product->$method(); // invoke the method
}


// while there  is a is_callable and method_exists

if (is_callable ( array ($product, $method )))  {
	print $product->$method(); // invoke the method  (NOTE: CAREFUL THAT YOU DON'T FORGET THE '$' IN FRONT OF THE 'method' NAME)

}

if (method_exists($product, $method)) { 
	print $product->$method(); // invoke the method  (NOTE: CAREFUL THAT YOU DON'T FORGET THE '$' IN FRONT OF THE 'method' NAME)
}

?>
```

as you can see from the above code, it is OK to declare the or NOT to declare the instance variable names.


## Php properties 

well, it seems that PHP does not take private variables as properties, it only takes the public variables as the properties, 
Example.


```

<?php

// Learn about proeprties 
// key here is to use the get_class method to return a string representing the class.
// methods that ca be covered in this situation include the following
//  1) Properties

class CdProduct { 

	/* -- private variables are not counted as the properties/variables
	private $subject;
	private $name;
	private $edition;
	private $discount;
	*/

	// Only public variables are counted.
	public $coverUrl;
	function CdProduct($subject, $name, $edition, $price, $discount) { 
		$this->subject= $subject;
		$this->name = $name;
		$this->eidtion = $edition;
		$this->discount = $discount;
		$coverUrl = 'http://news.163.com';
	}

}
```

print_r(get_class_vars('CdProduct'));
?>


Only the "coverUrl" are printed.


## what does this symbols mean in PHP

References: What does this symbol mean in PHP.

I encountered one `@` symbol the other day, and I looked over the Stack overflow, and this is the answer.

the `@` key is operator to suppress errror message by that expression can be ignored. (according to the following [PHP: Error Control Operators - Manual](http://php.net/manual/en/language.operators.errorcontrol.php))

```
<?php
/* Intentional file error */
$my_file = @file ('non_existent_file') or
    die ("Failed opening file: error was '$php_errormsg'");

// this works for any expression, not just functions:
$value = @$cache[$key];
// will not issue a notice if the index $key doesn't exist.

?>
```

General, please check with the Php manual.

References:
[operators - Reference - What does this symbol mean in PHP? - Stack Overflow](http://stackoverflow.com/questions/3737139/reference-what-does-this-symbol-mean-in-php)
[PHP: Error Control Operators - Manual](http://php.net/manual/en/language.operators.errorcontrol.php)
[PHP: PHP Manual - Manual](http://php.net/manual/en/index.php)


## an example to use the ReflectionAPI in PHP
well, so much for the discussion on basics of the PHP reflection, now let's review one of the example that uses Reflection API to simulate some runner.

the example uses a ModuleRunner as an example. here is the code. 


```
<?php

// Reflection
// Shows an example on how the reflection can be used to create some sort of module runner


// 3) ReflectionMethod

class Person { 
	public $name;


	function __construct($name) { 
		$this->name = $name;
	}

}

interface Module { 
	function execute();
}

class FtpModule implements Module {
	function setHost( $host ) {
		print "FtpModule::setHost(): $host\n";
	}
	function setUser( $user ) {
		print "FtpModule::setUser(): $user\n";
	}
	function execute() {
	// do things
	}
}


class PersonModule implements Module {
	function setPerson( Person $person ) {
		print "PersonModule::setPerson(): {$person->name}\n";
	}
	function execute() {
		// do things
	}
}


class ModuleRunner { 
	private $configData
		= array(
			"PersonModule" => array( 'person'=>'bob' ),
			"FtpModule" => array( 'host'
							=>'example.com',
						'user' =>'anon' )
		);

	private $modules = array();

	// set the module as thew 
	function init() {
		$interface = new ReflectionClass('Module');
		foreach ($this->configData as $modulename=>$params) {
			$module_class = new ReflectionClass( $modulename );
			if ( ! $module_class->isSubclassOf( $interface ) ) {
				throw new Exception( "unknown module type: $modulename" );
			}
			$module = $module_class->newInstance();
			foreach ( $module_class->getMethods() as $method ) {
				$this->handleMethod( $module, $method, $params );
				// we cover handleMethod() in a future listing!
			}
			array_push( $this->modules, $module );
		}
		// ...
	}


	function handleMethod(Module $module, ReflectionMethod $method, $params) {
		$name = $method->getName();
		$args = $method->getParameters();

		if ( count (args ) != 1 || substr ($name, 0, 3) != "set" ) {
			return false;
		}

		$property = strtolower( substr( $name, 3 ));
		if ( ! isset( $params[$property] ) ) {
			return false;
		}

		$arg_class = $args[0]->getClass();
		if ( empty( $arg_class ) ) {
			$method->invoke( $module, $params[$property] );
		} else { 
			$method->invoke( $module, $arg_class->newInstance( $params[$property] ) );
		}
	}

}


$test = new ModuleRunner();
$test->init();

?>

```

Basically it inspect the modues by inspecting class hierarchy and for each subclass to Module, find its methods aids with the config data, do the proper setter and then after the initialization is done. you can do a foreach loop to call `execute` on each of the module instance.
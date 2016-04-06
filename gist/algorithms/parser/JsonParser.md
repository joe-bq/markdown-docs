## introduction
this page will show you an implementation that uses the JsonParser to parse an string
the json parser is simple that it only handles the 

* string without "quote"
* nested dictionary


given an input 

```
"{name:joe,"
"gender:male,"
"address:{"
"city:shanghai,"
"street:hanghua,"
"number:285}"
"}";

```

## code

with test code and others.


```
package parser;

import java.util.Map;
import java.util.HashMap;

public class JsonParserExample {
	public static void main(String[] args) {
		String input = "{name:joe,"
				+      "gender:male,"
				+      "address:{"
				+      "city:shanghai,"
				+      "street:hanghua,"
				+      "number:285}"
				+      "}";
		
		
		JsonParserExample example = new JsonParserExample();
		Map<String, Object> result = example.parseJson(input);
		StringBuilder builder = new StringBuilder();
		example.printJson(result, builder);
		System.out.println(builder.toString());
	}
	
	public void printJsonEntry(Map.Entry<String, Object> jsonEntry, StringBuilder sb) {
		sb.append(jsonEntry.getKey());
		sb.append(":");
		Map<String, Object> jsonSubObject = null;
		String value = "";
		Object jsonEntryValue = jsonEntry.getValue();
		if (jsonEntryValue instanceof Map<?,?>) {
			jsonSubObject = (Map<String, Object>)jsonEntryValue;
			printJson(jsonSubObject, sb);
		} else {
			value = (String)jsonEntry.getValue();
			sb.append(value);
		}
	}
	
	public void printJson(Map<String, Object> json, StringBuilder sb) {
		
		sb.append("{");
		for (Map.Entry<String, Object> jsonEntry : json.entrySet()) { 
			printJsonEntry(jsonEntry, sb);
		}
		sb.append("}");
	}
	
	int index;
	public Map<String, Object> parseJson(String input) {
		Map<String, Object> map = new HashMap<String, Object>();
		boolean isKey = true;
		String key = "";
		String value_str = "";
		Map<String, Object> value = null;
		boolean isValueString = true;
		
		while (index < input.length()) {
			char c = input.charAt(index);
			index++;
			switch (c) {
			case '{':
				value = parseJson(input);
				isValueString = false;
				break;
			case '}':
				if (!isValueString) {
					if (!"".equals(key)) {
						map.put(key, value);
					} else {
						return value;
					}
				} else {
					if (!"".equals(key)) { 
						map.put(key, value_str);
					}
					
					return map;
				}
				
				isKey = true;
				key = "";
				value_str = "";
				value = null;
				isValueString = true;
				break;
			case ':':
				isKey = false;
				break;
			case ',':
				if (isValueString) {
					map.put(key, value_str);
				} else { 
					map.put(key, value);
				}
				
				isKey = true;
				key = "";
				value_str = "";
				value =null;
				break;
			default:
				if (isKey) { 
					key += c; 
				} else {
					value_str += c;
				}
				
				break;
			}
			
		}
		
		// value != null stands for top-level situation.
		if (value != null) return value;
		return map;
	}
}

```

well, this can work, but this is hard to extend , especially when we have decided to add more types, controls to make it a real-case JSONParser

to strive for that end, we can do the following way (the code below does exactly what is mentioned above);

```
package parser;
import java.util.Map;
import java.util.HashMap;

public class JsonParserExample2 {
	
	
	public static void main(String[] args) {
		JsonParserExample2 example2 = new JsonParserExample2();
		String input = "{name:joe,"
				+      "gender:male,"
				+      "address:{"
				+      "city:shanghai,"
				+      "street:hanghua,"
				+      "number:285}"
				+      "}";
		StringBuilder builder = new StringBuilder();
		example2.input = input.toCharArray();
		example2.index = 0;
		Map<String, Object> result = example2.parse();
		example2.printJson(result, builder);
		System.out.println(builder.toString());
	}

	public void printJsonEntry(Map.Entry<String, Object> jsonEntry, StringBuilder sb) {
		sb.append(jsonEntry.getKey());
		sb.append(":");
		Map<String, Object> jsonSubObject = null;
		String value = "";
		Object jsonEntryValue = jsonEntry.getValue();
		if (jsonEntryValue instanceof Map<?,?>) {
			jsonSubObject = (Map<String, Object>)jsonEntryValue;
			printJson(jsonSubObject, sb);
		} else {
			value = (String)jsonEntry.getValue();
			sb.append(value);
		}
	}
	
	public void printJson(Map<String, Object> json, StringBuilder sb) {
		
		sb.append("{");
		for (Map.Entry<String, Object> jsonEntry : json.entrySet()) { 
			printJsonEntry(jsonEntry, sb);
			sb.append(",");
		}
		sb.append("}");
	}
	
	
	/**
	 * var: input character arrays
	 */
	private char[] input;
	/**
	 * reading pointer
	 */
	private int index;
	
	public Map<String, Object> parse() { 
		
		Map<String, Object> map = new HashMap<String, Object>();
		eatSpaces();
		while (index < input.length){
			char c = input[index];
			switch (c) {
				case '{':
					index++;
					return parseObject();
			}
		}
		
		return map;
	}
	
	public Map<String, Object> parseObject() {
		
		Map<String, Object> map = new HashMap<String, Object>();
		Map<String, Object> value = null;
		String value_str = "";
		String key = "";
		while (index < input.length){ 
			char c = input[index];
			
			switch (c)  {
				case '{':
					index++;
					value = parseObject();
					break;
				case '}':
					index++;
					if (!"".equals(key)) {
						if (value != null) {
							map.put(key,  value);
						} else { 
							map.put(key, value_str);
						}
					}
					return map;
				case ',':
					index++;
					key = getNextToken();
					break;
				case ':':
					index++;
					char nextSymbol = lookAhead();
					switch (nextSymbol) {
					case '{':
						continue;
					default:
						value_str = getNextToken();
						map.put(key, value_str);
					}
					break;
				default:
					key = getNextToken();
					break;
			}
		}

		if (value != null) { return value; } 
		return map;
	}
	
	public String getNexKey() { 
		return getNextToken();
		
	}
	
	public String getNextValue() { 
		return getNextToken();
	}
	
	
	/**
	 * Look ahead to next non-empty
	 * this can renamed to skip blanks.
	 * @return
	 */
	public char lookAhead() {
		while (index < input.length) {
			char c = input[index];
			switch (c) {
				case ' ':
				case '\t':
					index++;
					continue;
				default:
					return c;
			}
		}
		
		return 0;
	}
		
	/**
	 * Get next available token.
	 * @return
	 */
	public String getNextToken() { 
		String token = "";
		outer:
		while (index < input.length) {
			char c = input[index];
			switch (c) {
				case ',':
				case '{':
				case '}':
				case ':':
					break outer;
				case ' ':
				case '\t':
					eatSpaces();
			}
			token += input[index];
			index++;
		}
		
		return token;
	}
	
	public void eatSpaces() { 
		while (index < input.length) {
			char c = input[index];
			switch (c) { 
				case '\t':
				case ' ':
					index++;
					break;
				default:
					return;
			}
		}
	}
	

}
```

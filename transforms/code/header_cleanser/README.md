# Header Cleanser Transform

The **Header Cleanser** module is a versatile tool designed to remove license and copyright headers from code files. It supports over 90 programming languages and utilizes the [ScanCode Toolkit](https://scancode-toolkit.readthedocs.io/en/stable/getting-started/install.html) to identify license and copyright information within the codebase.

## Input and Output

### Input
- **File Format**: Parquet file containing code.
- **Input Column**: The code should be in a column named `content`.
- **Sample Input**:  
  [Sample Input File](transforms/code/header_cleanser/python/test-data/input/test1.parquet)

### Output
- **File Format**: Parquet file with the updated code in the same column.
- **Sample Output**:  
  [Sample Output File](transforms/code/header_cleanser/python/test-data/expected/license-and-copyright-local/test1.parquet)

## Parameters

The following parameters can be adjusted to control the behavior of the extraction:

| Parameter Name            | Default Value | Description                                                         |
|---------------------------|---------------|---------------------------------------------------------------------|
| `content_column_name`      | `contents`    | Specifies the column name that holds the code to be processed.       |
| `copyright`                | `true`        | Set to `true` to remove copyright information from the code.         |
| `license`                  | `true`        | Set to `true` to remove license information from the code.           |

### CLI Syntax
When invoking the CLI, use the following syntax for these parameters:
```
--header_cleanser_<parameter_name>
```
For example:
```
--header_cleanser_content_column_name='content'
```

## Example

### Sample Input Code:
```java
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.jstevenperry.intro;

import java.util.logging.Logger;

// This is the main public class representing a Person
public class Person {
    private static final Logger logger = Logger.getLogger(Person.class.getName());

    private String name;
    private int age;
    private int height;
    private int weight;
    private String eyeColor;
    private String gender;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }

    public String getEyeColor() {
        return eyeColor;
    }

    public void setEyeColor(String eyeColor) {
        this.eyeColor = eyeColor;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public Person(String name, int age, int height, int weight, String eyeColor, String gender) {
        super();
        this.name = name;
        this.age = age;
        this.height = height;
        this.weight = weight;
        this.eyeColor = eyeColor;
        this.gender = gender;

        logger.info("Created Person object with name '" + getName() + "'");
    }
}
```

### Sample Output (with default parameters):
```java
package com.jstevenperry.intro;

import java.util.logging.Logger;

/// This is the main public class representing a Person
public class Person {

    private static final Logger logger = Logger.getLogger(Person.class.getName());

    private String name;
    private int age;
    private int height;
    private int weight;
    private String eyeColor;
    private String gender;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }

    public String getEyeColor() {
        return eyeColor;
    }

    public void setEyeColor(String eyeColor) {
        this.eyeColor = eyeColor;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public Person(String name, int age, int height, int weight, String eyeColor, String gender) {
        super();
        this.name = name;
        this.age = age;
        this.height = height;
        this.weight = weight;
        this.eyeColor = eyeColor;
        this.gender = gender;

        logger.info("Created Person object with name '" + getName() + "'");
    }
}
```

## Different Runtimes

- **[Python](python/README.md)**: Provides the base Python-based transformation implementation.
- **[Ray](ray/README.md)**: Enables running the base Python transformation in a Ray runtime.
- **[KFP Ray](kfp_ray/README.md)**: Enables running the Ray Docker image in a Kubernetes cluster using a generated YAML file.

## Sample Notebook

Check out the [example notebook](notebooks/header_cleanser.ipynb) for further details.


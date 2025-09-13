# Grant Robinson's Heredity Project
This is a simple AI project that uses probability to infer the likelihood that each person in a family has a given gene, and whether
or not they exhibit a trait associated with the gene based on a family tree and known evidence.
## What this project is
<ul>
  <li>Project in CS50's Introduction to Artificial Intelligence with Python</li>
  <li> Computes the probability distribution of how many copies of a gene each person has (0, 1, or 2), and if each person exhibits the trait (Yes/No)
  </li>
  <li>Produces normalized distributions for each person after calculating the probability distribution for each event</li>
</ul>
## How to use it
<ul>
  <li>Only requires Python 3 (any version of it is fine)</li>
  <li>
    <p> Getting Started: </p>
    <ol>
      <li>Clone the repository (e.g. git clone https://github.com/grantMU3000/Heredity.git </li>
      <li> Run the program with a CSV dataset (e.g. python heredity.py data/family0.csv)</li>
    </ol>
  </li>
  <li>
    <p>Input CSV Format:</p>
    <ul>
      <li> Columns: Name, Mother, Father, Trait </li>
      <li> If mother/father is blank, then the person is simply just a parent </li>
      <li> Trait is 1 (Has trait), 0 (Doesn't), or blank (unknown) </li>
    </ul>
  </li>
  <li>
    <p> Example: </p>
    <p> python heredity.py data/family0.csv </p>
    <p> Example output: <br>
      Harry:
  Gene:
    2: 0.0092
    1: 0.4557
    0: 0.5351
  Trait:
    True: 0.2665
    False: 0.7335
James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000
    False: 0.0000
Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000
    False: 1.0000
    </p>
  </li>
</ul>

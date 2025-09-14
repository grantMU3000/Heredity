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
      Harry:<br>
      <ul>
        Gene: <br>
        <ul>
          2: 0.0092 <br>
          1: 0.4557 <br>
          0: 0.5351 <br>
        </ul>
        Trait: <br>
        <ul>
          True: 0.2665 <br>
          False: 0.7335 <br>
        </ul>
      </ul>
James: <br>
  <ul>
  Gene: <br>
    <ul>
    2: 0.1976 <br>
    1: 0.5106 <br>
    0: 0.2918 <br>
    </ul>
  Trait:<br>
    <ul>
    True: 1.0000<br>
    False: 0.0000<br>
    </ul>
  </ul>
Lily:<br>
  <ul>
  Gene:<br>
    <ul>
    2: 0.0036<br>
    1: 0.0136<br>
    0: 0.9827<br>
    </ul>
  Trait:<br>
    <ul>
    True: 0.0000<br>
    False: 1.0000<br>
    </ul>
    </p>
  </li>
</ul>

## How I made it
The main method, load data, and powerset functions were all provided for me pre-made. I was also provided with a dictionary of probabilities to base my calculations off of. I then implemented the rest of the functions that were provided to me. Those are down below.
<ul>
  <li>
    <p>Joint Probability</p>
    <ul>
      <li> Computed the probability of a person having 0-2 trait-associated genes. (Based on their parent's gene counts. If they don't have parents, it's unconditional.) </li>
      <li> Computed the probability of a person exhibiting the trait given the count of their trait-associated genes. </li>
      <li> Used the above two computations to calculate the likelihood that a person has x amount of genes and exhibits the trait associated with the gene. </li>
      <li> For each person in this event, I multiplied the everyone's probability together to get the joint probability, and returned this. </li>
    </ul>
  </li>
</ul>

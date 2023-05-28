
**This tool is based on an unreleased research prototype. Please do not your share 
your project publicly (e.g. on Github). Thank you!**

<p align="center"><a><img width="170" alt="portfolio_view" align="center" src="misc/et-picture.png"></a></p>

</p>

E.T.
====== 


### 1. Prepare grammar

```
bin/prepare_grammar <antlr_grammar>
```

where `<antlr_grammar>` is a `.g4` file. 


### 2. Run exhaustive enumeration

```
bin/enumerate <binary_clis> <depth>
```

- `<binary_clis>` is a sequence of commands enclosed by punctuation marks and 
   separated by semicola 

- `<depth>` is the depth bound for the enumerator

# Example 

```
./bin/prepare_grammar smtlib_grammars/Strings.g4
./bin/enumerate "z3 model_validate=true;cvc5 -q --check-models --strings-exp" 4
```


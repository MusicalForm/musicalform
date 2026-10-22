**Label:**

![Label](diagram/Label.png)

```
Label    ::= ( Name ':' )? ( FormLabel | PlaceholderLabel ) ( '-' FormLabel )*
```

**FormLabel:**

![FormLabel](diagram/FormLabel.png)

```
FormLabel
         ::= Form MaterialBrackets? Combinator?
```

referenced by:

* Label

**PlaceholderLabel:**

![PlaceholderLabel](diagram/PlaceholderLabel.png)

```
PlaceholderLabel
         ::= '%' Shorthand? MaterialBrackets?
```

referenced by:

* Label

**Name:**

![Name](diagram/Name.png)

```
Name     ::= [a-zA-Z0-9'_]+
```

referenced by:

* Entry
* Label

**Form:**

![Form](diagram/Form.png)

```
Form     ::= FunctionLabel ( '|' TypeExp )? '?'?
```

referenced by:

* FormLabel

**FunctionLabel:**

![FunctionLabel](diagram/FunctionLabel.png)

```
FunctionLabel
         ::= FunctionExpr ( Combinator FunctionExpr )?
```

referenced by:

* Form

**Combinator:**

![Combinator](diagram/Combinator.png)

```
Combinator
         ::= '/'
           | '>'
```

referenced by:

* FormLabel
* FunctionLabel

**FunctionExpr:**

![FunctionExpr](diagram/FunctionExpr.png)

```
FunctionExpr
         ::= Function Shorthand?
```

referenced by:

* FunctionLabel

**Function:**

![Function](diagram/Function.png)

```
Function ::= '"' FunctionName '"'
           | FunctionName
```

referenced by:

* FunctionExpr

**FunctionName:**

![FunctionName](diagram/FunctionName.png)

```
FunctionName
         ::= SpecificFunction
           | GenericFunction
```

referenced by:

* Function

**GenericFunction:**

![GenericFunction](diagram/GenericFunction.png)

```
GenericFunction
         ::= ( Cardinality '_'? )? Unit
```

referenced by:

* FunctionName

**Cardinality:**

![Cardinality](diagram/Cardinality.png)

```
Cardinality
         ::= ( '1' [0-9] | [04-9] ) 'th'
           | [2-9] ( '1st' | '2nd' | '3rd' | [04-9] 'th' )
           | '1st'
           | '2nd'
           | '3rd'
```

referenced by:

* GenericFunction

**Unit:**

![Unit](diagram/Unit.png)

```
Unit     ::= 'unit'
           | 'x'
           | 'part'
           | 'section'
           | 'sec'
           | 'phrase'
           | 'sub-phrase'
           | 'idea'
           | 'work'
           | 'movement'
           | 'mvt'
           | 'piece'
           | 'zone'
           | 'theme'
           | 'album'
           | 'song'
           | 'cycle'
           | 'group'
```

referenced by:

* FormalType
* GenericFunction

**SpecificFunction:**

![SpecificFunction](diagram/SpecificFunction.png)

```
SpecificFunction
         ::= 'antecedent'
           | 'ant'
           | 'after-the-end'
           | 'ate'
           | 'basic_idea'
           | 'bi'
           | 'beginning'
           | 'beg'
           | 'cadential_idea'
           | 'cadi'
           | 'cadential_phrase'
           | 'cad'
           | 'compound_basic_idea'
           | 'cbi'
           | 'codetta'
           | 'cdta'
           | 'contrasting_idea'
           | 'ci'
           | 'contrasting_middle'
           | 'cm'
           | 'closing_theme'
           | 'cls'
           | 'coda'
           | 'consequent'
           | 'cons'
           | 'continuation_idea'
           | 'continuation'
           | 'conti'
           | 'cont'
           | 'development_section'
           | 'dev'
           | 'end'
           | 'essential_expositional_closure'
           | 'eec'
           | 'essential_sonata_closure'
           | 'esc'
           | 'exposition'
           | 'exp'
           | 'fragmentation'
           | 'frag'
           | 'introduction'
           | 'intro'
           | 'lead-in'
           | 'lin'
           | 'middle'
           | 'mid'
           | 'model'
           | 'mod'
           | 'postcadential'
           | 'pcad'
           | 'presentation'
           | 'pres'
           | 'primary_theme_zone'
           | 'primary_theme'
           | 'ptz'
           | 'pt'
           | 'recapitulation'
           | 'recap'
           | 'ritornello'
           | 'rit'
           | 'retransition'
           | 'rtr'
           | 'standing_on_the_dominant'
           | 'sod'
           | 'secondary_theme_zone'
           | 'secondary_theme'
           | 'stz'
           | 'st'
           | 'sequence'
           | 'seq'
           | 'transition'
           | 'tr'
```

referenced by:

* FunctionName

**TypeExp:**

![TypeExp](diagram/TypeExp.png)

```
TypeExp  ::= '"' FormalType '"'
           | FormalType
```

referenced by:

* Form

**FormalType:**

![FormalType](diagram/FormalType.png)

```
FormalType
         ::= 'hybrid1'
           | 'hyb1'
           | 'hybrid2'
           | 'hyb2'
           | 'hybrid3'
           | 'hyb3'
           | 'hybrid4'
           | 'hyb4'
           | 'model_sequence'
           | 'modseq'
           | 'period'
           | 'pd'
           | 'repeated' '_'? Unit
           | 'ritornello_form'
           | 'ritornello'
           | 'rondo_form'
           | 'rondo'
           | 'sentence'
           | 'sent'
           | 'sequence'
           | 'seq'
           | 'sonata_form'
           | 'sonata'
           | 'unary_form'
           | 'unary'
           | 'simple_binary.balanced'
           | 'simple_binary'
           | 'rounded_binary'
           | 'ternary.through_composed'
           | 'ternary.da_capo'
           | 'ternary'
```

referenced by:

* TypeExp

**MaterialBrackets:**

![MaterialBrackets](diagram/MaterialBrackets.png)

```
MaterialBrackets
         ::= '[' MaterialPositions ']'
```

referenced by:

* FormLabel
* PlaceholderLabel

**MaterialPositions:**

![MaterialPositions](diagram/MaterialPositions.png)

```
MaterialPositions
         ::= TargetOnly
           | MaterialRef ( ',' MaterialRef )?
           | SourceOnly
```

referenced by:

* MaterialBrackets

**TargetOnly:**

![TargetOnly](diagram/TargetOnly.png)

```
TargetOnly
         ::= ',' MaterialRef
```

referenced by:

* MaterialPositions

**SourceOnly:**

![SourceOnly](diagram/SourceOnly.png)

```
SourceOnly
         ::= MaterialRef ','
```

referenced by:

* MaterialPositions

**MaterialRef:**

![MaterialRef](diagram/MaterialRef.png)

```
MaterialRef
         ::= '[' Concatenation ']'
           | '(' Concatenation ')'
           | Combination
           | Entry
```

referenced by:

* MaterialPositions
* SourceOnly
* TargetOnly

**Concatenation:**

![Concatenation](diagram/Concatenation.png)

```
Concatenation
         ::= Entry ( ',' Entry )+
```

referenced by:

* MaterialRef

**Combination:**

![Combination](diagram/Combination.png)

```
Combination
         ::= Entry ( '&' Entry )+
```

referenced by:

* MaterialRef

**Shorthand:**

![Shorthand](diagram/Shorthand.png)

```
Shorthand
         ::= MaterialRelations
```

referenced by:

* FunctionExpr
* PlaceholderLabel

**MaterialKeyword:**

![MaterialKeyword](diagram/MaterialKeyword.png)

```
MaterialKeyword
         ::= '$' ( 'adapt' | 'aug' | 'comb' | 'conc' | 'dim' | 'ext' | 'inv' | 'orn'
                  | 'part' | 'rep' | 'retr' | 'transp' | 'var' )
```

referenced by:

* MaterialRelations

**MaterialOperator:**

![MaterialOperator](diagram/MaterialOperator.png)

```
MaterialOperator
         ::= [!*~^°+]
```

referenced by:

* MaterialRelations

**MaterialRelations:**

![MaterialRelations](diagram/MaterialRelations.png)

```
MaterialRelations
         ::= ( MaterialKeyword | MaterialOperator )+
```

referenced by:

* Entry
* Shorthand

**Entry:**

![Entry](diagram/Entry.png)

```
Entry    ::= ( '"' Name '"' | Name ) MaterialRelations?
```

referenced by:

* Combination
* Concatenation
* MaterialRef

## 
![rr-2.6](diagram/rr-2.6.png) <sup>generated by [RR - Railroad Diagram Generator][RR]</sup>

[RR]: https://www.bottlecaps.de/rr/ui
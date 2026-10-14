**Label:**

![Label](diagram/Label.png)

```
Label    ::= ( Name ':' )? ( FormLabel | PlaceholderLabel ) ( '-' FormLabel )*
```

**FormLabel:**

![FormLabel](diagram/FormLabel.png)

```
FormLabel
         ::= Form MaterialBrackets?
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
Name     ::= [a-zA-Z0-9']+
```

referenced by:

* Entry
* Label

**Form:**

![Form](diagram/Form.png)

```
Form     ::= FunctionLabel ( '|' TypeExp )?
```

referenced by:

* FormLabel

**FunctionLabel:**

![FunctionLabel](diagram/FunctionLabel.png)

```
FunctionLabel
         ::= FunctionExpr ( '/' | '>' FunctionExpr? )?
```

referenced by:

* Form

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
         ::= GenericFunction
           | SpecificFunction
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
         ::= '1st'
           | '2nd'
           | '3rd'
           | '4th'
           | '5th'
           | '6th'
           | '7th'
           | '8th'
           | '9th'
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
           | 'phrase'
           | 'sub-phrase'
           | 'idea'
           | 'work'
           | 'movement'
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
           | 'basic idea'
           | 'bi'
           | 'cadential idea'
           | 'cad'
           | 'compound basic idea'
           | 'cbi'
           | 'codetta'
           | 'cdta'
           | 'contrasting idea'
           | 'ci'
           | 'closing theme'
           | 'cls'
           | 'coda'
           | 'consequent'
           | 'cons'
           | 'continuation idea'
           | 'continuation'
           | 'conti'
           | 'cont'
           | 'development section'
           | 'dev'
           | 'essential expositional closure'
           | 'eec'
           | 'essential sonata closure'
           | 'esc'
           | 'exposition'
           | 'exp'
           | 'fragmentation'
           | 'frag'
           | 'introduction'
           | 'intro'
           | 'lead-in'
           | 'lin'
           | 'model'
           | 'mod'
           | 'movement'
           | 'mvt'
           | 'postcadential'
           | 'pcad'
           | 'presentation'
           | 'pres'
           | 'primary theme zone'
           | 'primary theme'
           | 'ptz'
           | 'pt'
           | 'recapitulation'
           | 'recap'
           | 'ritornello'
           | 'rit'
           | 'retransition'
           | 'rtr'
           | 'secondary theme zone'
           | 'secondary theme'
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
           | 'period'
           | 'pd'
           | 'repeated' '_'? Unit
           | 'ritornello form'
           | 'ritornello'
           | 'rondo form'
           | 'rondo'
           | 'sentence'
           | 'sent'
           | 'sequence'
           | 'seq'
           | 'sonata form'
           | 'sonata'
           | 'unary form'
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
           | Concatenation
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

**Shorthand:**

![Shorthand](diagram/Shorthand.png)

```
Shorthand
         ::= MaterialOperators
```

referenced by:

* FunctionExpr
* PlaceholderLabel

**MaterialOperators:**

![MaterialOperators](diagram/MaterialOperators.png)

```
MaterialOperators
         ::= [!*~^°+]+
```

referenced by:

* Entry
* Shorthand

**Entry:**

![Entry](diagram/Entry.png)

```
Entry    ::= ( '"' Name '"' | Name ) MaterialOperators?
```

referenced by:

* Concatenation
* MaterialRef

##
![rr-2.6](diagram/rr-2.6.png) <sup>generated by [RR - Railroad Diagram Generator][RR]</sup>

[RR]: https://www.bottlecaps.de/rr/ui

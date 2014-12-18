
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'SGU\xe3O\xf8\x17B\x1a\x9aL=F\x1d\x95I'
    
_lr_action_items = {'AND':([10,11,12,15,16,25,26,32,33,34,37,45,49,],[22,-25,-24,-23,-27,22,-22,22,22,22,-26,-19,22,]),'OR':([10,11,12,15,16,25,26,32,33,34,37,45,49,],[23,-25,-24,-23,-27,23,-22,23,23,23,-26,-19,23,]),'RPAREN':([11,12,15,16,24,25,26,32,33,34,35,36,37,40,42,44,45,48,49,52,53,],[-25,-24,-23,-27,-28,37,-22,-20,-21,-28,45,-15,-26,47,-14,-17,-19,-28,-28,54,-16,]),'STR':([28,],[39,]),'GRAPH':([0,2,3,4,5,8,10,11,12,15,16,17,18,19,20,26,27,30,32,33,37,39,45,47,50,51,54,],[6,-3,-5,6,-4,-6,-18,-25,-24,-23,-27,-1,-2,-28,-7,-22,-9,-13,-20,-21,-26,-12,-19,-28,-11,-8,-10,]),'NUMBER':([1,13,14,22,23,24,29,38,43,48,],[11,11,11,11,11,11,40,11,11,11,]),'ID':([1,6,7,13,14,16,21,22,23,24,31,38,43,48,],[16,16,16,16,16,-27,16,16,16,16,16,16,16,16,]),'ASSERT':([0,2,3,4,5,8,10,11,12,15,16,17,18,19,20,26,27,30,32,33,37,39,45,47,50,51,54,],[1,-3,-5,1,-4,-6,-18,-25,-24,-23,-27,-1,-2,-28,-7,-22,-9,-13,-20,-21,-26,-12,-19,-28,-11,-8,-10,]),'EQUALS':([16,19,47,],[-27,28,28,]),'BOOL':([0,2,3,4,5,8,10,11,12,15,16,17,18,19,20,26,27,30,32,33,37,39,45,47,50,51,54,],[7,-3,-5,7,-4,-6,-18,-25,-24,-23,-27,-1,-2,-28,-7,-22,-9,-13,-20,-21,-26,-12,-19,-28,-11,-8,-10,]),'LPAREN':([1,12,13,14,16,19,22,23,24,38,41,43,48,],[13,24,13,13,-27,29,13,13,13,13,48,13,13,]),'LBRACKET':([28,],[38,]),'NOT':([1,13,14,22,23,24,38,43,48,],[14,14,14,14,14,14,14,14,14,]),'COMMA':([11,12,15,16,26,32,33,34,37,45,49,],[-25,-24,-23,-27,-22,-20,-21,43,-26,-19,43,]),'RBRACKET':([11,12,15,16,26,32,33,34,36,37,38,42,44,45,46,49,53,],[-25,-24,-23,-27,-22,-20,-21,-28,-15,-26,-28,-14,-17,-19,50,-28,-16,]),'SAGEGRAPH':([0,2,3,4,5,8,10,11,12,15,16,17,18,19,20,26,27,30,32,33,37,39,45,47,50,51,54,],[9,-3,-5,9,-4,-6,-18,-25,-24,-23,-27,-1,-2,-28,-7,-22,-9,-13,-20,-21,-26,-12,-19,-28,-11,-8,-10,]),'DOT':([9,],[21,]),'$end':([2,3,4,5,8,10,11,12,15,16,17,18,19,20,26,27,30,32,33,37,39,45,47,50,51,54,],[-3,-5,0,-4,-6,-18,-25,-24,-23,-27,-1,-2,-28,-7,-22,-9,-13,-20,-21,-26,-12,-19,-28,-11,-8,-10,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'graphdef':([19,47,],[27,51,]),'nonemptylist':([34,49,],[42,53,]),'expr':([1,13,14,22,23,24,38,43,48,],[10,25,26,32,33,34,34,49,34,]),'vardecl':([0,4,],[2,17,]),'boolvardecl':([0,4,],[3,3,]),'idprod':([1,6,7,13,14,21,22,23,24,31,38,43,48,],[12,19,20,12,12,31,12,12,12,41,12,12,12,]),'program':([0,],[4,]),'assertdecl':([0,4,],[5,18,]),'operation':([1,13,14,22,23,24,38,43,48,],[15,15,15,15,15,15,15,15,15,]),'graphvardecl':([0,4,],[8,8,]),'exprlist':([24,38,48,],[35,46,52,]),'empty':([19,24,34,38,47,48,49,],[30,36,44,36,30,36,44,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> program vardecl','program',2,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',23),
  ('program -> program assertdecl','program',2,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',24),
  ('program -> vardecl','program',1,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',25),
  ('program -> assertdecl','program',1,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',26),
  ('vardecl -> boolvardecl','vardecl',1,'p_vardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',35),
  ('vardecl -> graphvardecl','vardecl',1,'p_vardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',36),
  ('boolvardecl -> BOOL idprod','boolvardecl',2,'p_boolvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',41),
  ('graphvardecl -> GRAPH idprod LPAREN NUMBER RPAREN graphdef','graphvardecl',6,'p_graphvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',47),
  ('graphvardecl -> GRAPH idprod graphdef','graphvardecl',3,'p_graphvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',48),
  ('graphvardecl -> SAGEGRAPH DOT idprod idprod LPAREN exprlist RPAREN','graphvardecl',7,'p_graphvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',49),
  ('graphdef -> EQUALS LBRACKET exprlist RBRACKET','graphdef',4,'p_graphdef','/home/ezulkosk/git/sagesat/src/front/parser.py',59),
  ('graphdef -> EQUALS STR','graphdef',2,'p_graphdef','/home/ezulkosk/git/sagesat/src/front/parser.py',60),
  ('graphdef -> empty','graphdef',1,'p_graphdef','/home/ezulkosk/git/sagesat/src/front/parser.py',61),
  ('exprlist -> expr nonemptylist','exprlist',2,'p_exprlist','/home/ezulkosk/git/sagesat/src/front/parser.py',70),
  ('exprlist -> empty','exprlist',1,'p_exprlist','/home/ezulkosk/git/sagesat/src/front/parser.py',71),
  ('nonemptylist -> COMMA expr nonemptylist','nonemptylist',3,'p_nonemptylist','/home/ezulkosk/git/sagesat/src/front/parser.py',83),
  ('nonemptylist -> empty','nonemptylist',1,'p_nonemptylist','/home/ezulkosk/git/sagesat/src/front/parser.py',84),
  ('assertdecl -> ASSERT expr','assertdecl',2,'p_assertdecl','/home/ezulkosk/git/sagesat/src/front/parser.py',94),
  ('operation -> idprod LPAREN exprlist RPAREN','operation',4,'p_operation','/home/ezulkosk/git/sagesat/src/front/parser.py',98),
  ('expr -> expr AND expr','expr',3,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',103),
  ('expr -> expr OR expr','expr',3,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',104),
  ('expr -> NOT expr','expr',2,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',105),
  ('expr -> operation','expr',1,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',106),
  ('expr -> idprod','expr',1,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',107),
  ('expr -> NUMBER','expr',1,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',108),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expression_group','/home/ezulkosk/git/sagesat/src/front/parser.py',120),
  ('idprod -> ID','idprod',1,'p_ID','/home/ezulkosk/git/sagesat/src/front/parser.py',124),
  ('empty -> <empty>','empty',0,'p_empty','/home/ezulkosk/git/sagesat/src/front/parser.py',128),
]

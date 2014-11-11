
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'v\xaa\xb6\xd5\xff\x05\xbb\xb3\x14\xf9\x88\xa4O\xa7\x14?'
    
_lr_action_items = {'AND':([10,11,12,15,16,25,26,29,30,31,34,40,43,],[22,-23,-22,-21,-25,22,22,22,22,22,-24,-17,22,]),'OR':([10,11,12,15,16,25,26,29,30,31,34,40,43,],[23,-23,-22,-21,-25,23,23,23,23,23,-24,-17,23,]),'RPAREN':([11,12,15,16,24,25,26,29,30,31,32,33,34,35,37,39,40,42,43,47,48,],[-23,-22,-21,-25,-26,34,-20,-18,-19,-26,40,-13,-24,41,-12,-15,-17,-26,-26,50,-14,]),'GRAPH':([0,2,3,4,5,8,10,11,12,15,16,17,18,20,26,29,30,34,40,41,44,46,50,52,],[6,-3,-5,6,-4,-6,-16,-23,-22,-21,-25,-1,-2,-7,-20,-18,-19,-24,-17,-26,-8,-11,-9,-10,]),'NUMBER':([1,13,14,22,23,24,27,38,42,49,],[11,11,11,11,11,11,35,11,11,11,]),'ID':([1,6,7,13,14,16,21,22,23,24,28,38,42,49,],[16,16,16,16,16,-25,16,16,16,16,16,16,16,16,]),'ASSERT':([0,2,3,4,5,8,10,11,12,15,16,17,18,20,26,29,30,34,40,41,44,46,50,52,],[1,-3,-5,1,-4,-6,-16,-23,-22,-21,-25,-1,-2,-7,-20,-18,-19,-24,-17,-26,-8,-11,-9,-10,]),'EQUALS':([41,],[45,]),'BOOL':([0,2,3,4,5,8,10,11,12,15,16,17,18,20,26,29,30,34,40,41,44,46,50,52,],[7,-3,-5,7,-4,-6,-16,-23,-22,-21,-25,-1,-2,-7,-20,-18,-19,-24,-17,-26,-8,-11,-9,-10,]),'LPAREN':([1,12,13,14,16,19,22,23,24,36,38,42,49,],[13,24,13,13,-25,27,13,13,13,42,13,13,13,]),'LBRACKET':([45,],[49,]),'NOT':([1,13,14,22,23,24,38,42,49,],[14,14,14,14,14,14,14,14,14,]),'COMMA':([11,12,15,16,26,29,30,31,34,40,43,],[-23,-22,-21,-25,-20,-18,-19,38,-24,-17,38,]),'RBRACKET':([11,12,15,16,26,29,30,31,33,34,37,39,40,43,48,49,51,],[-23,-22,-21,-25,-20,-18,-19,-26,-13,-24,-12,-15,-17,-26,-14,-26,52,]),'SAGEGRAPH':([0,2,3,4,5,8,10,11,12,15,16,17,18,20,26,29,30,34,40,41,44,46,50,52,],[9,-3,-5,9,-4,-6,-16,-23,-22,-21,-25,-1,-2,-7,-20,-18,-19,-24,-17,-26,-8,-11,-9,-10,]),'DOT':([9,],[21,]),'$end':([2,3,4,5,8,10,11,12,15,16,17,18,20,26,29,30,34,40,41,44,46,50,52,],[-3,-5,0,-4,-6,-16,-23,-22,-21,-25,-1,-2,-7,-20,-18,-19,-24,-17,-26,-8,-11,-9,-10,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'graphdef':([41,],[44,]),'nonemptylist':([31,43,],[37,48,]),'expr':([1,13,14,22,23,24,38,42,49,],[10,25,26,29,30,31,43,31,31,]),'vardecl':([0,4,],[2,17,]),'boolvardecl':([0,4,],[3,3,]),'idprod':([1,6,7,13,14,21,22,23,24,28,38,42,49,],[12,19,20,12,12,28,12,12,12,36,12,12,12,]),'program':([0,],[4,]),'assertdecl':([0,4,],[5,18,]),'operation':([1,13,14,22,23,24,38,42,49,],[15,15,15,15,15,15,15,15,15,]),'graphvardecl':([0,4,],[8,8,]),'exprlist':([24,42,49,],[32,47,51,]),'empty':([24,31,41,42,43,49,],[33,39,46,33,39,33,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> program vardecl','program',2,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',22),
  ('program -> program assertdecl','program',2,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',23),
  ('program -> vardecl','program',1,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',24),
  ('program -> assertdecl','program',1,'p_program','/home/ezulkosk/git/sagesat/src/front/parser.py',25),
  ('vardecl -> boolvardecl','vardecl',1,'p_vardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',34),
  ('vardecl -> graphvardecl','vardecl',1,'p_vardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',35),
  ('boolvardecl -> BOOL idprod','boolvardecl',2,'p_boolvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',40),
  ('graphvardecl -> GRAPH idprod LPAREN NUMBER RPAREN graphdef','graphvardecl',6,'p_graphvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',46),
  ('graphvardecl -> SAGEGRAPH DOT idprod idprod LPAREN exprlist RPAREN','graphvardecl',7,'p_graphvardecl','/home/ezulkosk/git/sagesat/src/front/parser.py',47),
  ('graphdef -> EQUALS LBRACKET exprlist RBRACKET','graphdef',4,'p_graphdef','/home/ezulkosk/git/sagesat/src/front/parser.py',57),
  ('graphdef -> empty','graphdef',1,'p_graphdef','/home/ezulkosk/git/sagesat/src/front/parser.py',58),
  ('exprlist -> expr nonemptylist','exprlist',2,'p_exprlist','/home/ezulkosk/git/sagesat/src/front/parser.py',67),
  ('exprlist -> empty','exprlist',1,'p_exprlist','/home/ezulkosk/git/sagesat/src/front/parser.py',68),
  ('nonemptylist -> COMMA expr nonemptylist','nonemptylist',3,'p_nonemptylist','/home/ezulkosk/git/sagesat/src/front/parser.py',80),
  ('nonemptylist -> empty','nonemptylist',1,'p_nonemptylist','/home/ezulkosk/git/sagesat/src/front/parser.py',81),
  ('assertdecl -> ASSERT expr','assertdecl',2,'p_assertdecl','/home/ezulkosk/git/sagesat/src/front/parser.py',91),
  ('operation -> idprod LPAREN exprlist RPAREN','operation',4,'p_operation','/home/ezulkosk/git/sagesat/src/front/parser.py',95),
  ('expr -> expr AND expr','expr',3,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',100),
  ('expr -> expr OR expr','expr',3,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',101),
  ('expr -> NOT expr','expr',2,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',102),
  ('expr -> operation','expr',1,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',103),
  ('expr -> idprod','expr',1,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',104),
  ('expr -> NUMBER','expr',1,'p_expression','/home/ezulkosk/git/sagesat/src/front/parser.py',105),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expression_group','/home/ezulkosk/git/sagesat/src/front/parser.py',117),
  ('idprod -> ID','idprod',1,'p_ID','/home/ezulkosk/git/sagesat/src/front/parser.py',132),
  ('empty -> <empty>','empty',0,'p_empty','/home/ezulkosk/git/sagesat/src/front/parser.py',136),
]

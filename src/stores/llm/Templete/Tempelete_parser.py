import os


class TempleteParser:
    def __init__(self, language: str=None ,defult_language ="arb"):

        self.curent_path=os.path.dirname(os.path.abspath(__file__))
        self.defult_language = defult_language
        self.language = None
        self.set_language(language)

    def set_language(self, language: str) :

        if not language:
          self.language=self.defult_language

        language_path=os.path.join(self.curent_path,"locales",language)
       
        if  language and os.path.exists(language_path):
            self.language=language

        else:
            self.language=self.defult_language

    def get(self,group :str ,key :str ,var:dict={}):

        if not group or not key:
            return None
        
        group_path=os.path.join(self.curent_path,"locales",self.language,f"{group}.py")
        target_language=self.language
        if not os.path.exists(group_path):
                    group_path=os.path.join(self.curent_path,"locales",self.defult_language,f"{group}.py")
                    target_language=self.defult_language
        
        if not os.path.exists(group_path):
            return None
        
        # import the group module
        group_module=__import__(f"stores.llm.Templete.locales.{self.language}.{group}", fromlist=[group])

        if not group_module:
            return None 
        
        key_atribute=getattr(group_module,key)

        return key_atribute.substitute(var) 
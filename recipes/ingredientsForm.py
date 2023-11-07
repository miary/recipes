from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML


class IngredForm(forms.Form):
    staple = forms.MultipleChoiceField(
        choices=(
            ("casava", "Casava"),
            ("plantain", "Plantain"),
            ("jollof rice","Jollof rice"),
        ),
        widget=forms.CheckboxSelectMultiple,
    )
            
    main = forms.MultipleChoiceField(
        choices=(
            ("brown beans", "Brown beans"),
            ("Iru","Iru"),
            ("sorghum","Sorghum"),
            ("black-eyed peas","Black-eyed peas"),
            ("yams","Yams"),
            ("Okra","Okra"),
            ("millet","Millet"),
            ("fonio","Fonio"),
        ),
        widget=forms.CheckboxSelectMultiple,
    )
    
    leaves = forms.MultipleChoiceField(
        choices=(
            ("Bitter leaf","Bitter leaf"),
            ("Zobo leaf","Zobo leaf"),
            ("Pumplin leaf","Pumplin leaf"),
            ("Moringa leaf","Moringa leaf"),
            ("Uziza leaf","Uziza leaf"),
            ("Mitoo slender leaf","Mitoo slender leaf")
            
        ),
        widget=forms.CheckboxSelectMultiple,
    )
    
    meat = forms.MultipleChoiceField(
        choices=(
            ("chicken","Chicken"),
            ("goat","Goat"),
            ("beef","Cow meat"),
            ("lamb","Lamb"),
            ("Guinea fowl","Guinea fowl")
        ),
        widget=forms.RadioSelect,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('ingredDisplay')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit','Submit'))
        self.helper.layout = Layout(
            Fieldset(
                'Recipe Ingredients',
                Div('staple', css_class='custom-class'),
                Div('leaves', css_class='custom-class'),
                Div('main', css_class='custom-class'),
                Div('meat', css_class='custom-class'),
            ),
            HTML("<p>Select from the ingredients listed above.</p>"),
        )
        
      
    
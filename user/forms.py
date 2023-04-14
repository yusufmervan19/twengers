from django import forms



class LoginForm(forms.Form):
    username=forms.CharField(label="Kullanıcı adı",widget=forms.TextInput(attrs={'placeholder':"Your Username","class":"w-full py-4 px-6 rounded-xl"}))
    password=forms.CharField(label="Parola",widget=forms.PasswordInput(attrs={'placeholder':"Your Password","class":"w-full py-4 px-6 rounded-xl"}))
    


class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50,label="Username",widget=forms.TextInput(attrs={'placeholder':"Your Username","class":"w-full py-4 px-6 rounded-xl"}))
    password=forms.CharField(max_length=20,label="Password",widget=forms.PasswordInput(attrs={'placeholder':"Your Password","class":"w-full py-4 px-6 rounded-xl"}))
    confirm=forms.CharField(max_length=20,label="Password Correction",widget=forms.PasswordInput(attrs={'placeholder':"Repeat Password","class":"w-full py-4 px-6 rounded-xl"}))
    

    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        confirm=self.cleaned_data.get("confirm")

        if password and confirm and password!=confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor...")
        
        values={
            "username":username,
            "password":password,
        
        }
        return values
    
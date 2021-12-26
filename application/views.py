from django.contrib.messages.api import error, success
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import CreateUserForm
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# FUNCTION FOR DEFINING THE HOME PAGE 
def index(request):
    return render(request, 'index.html')


# FUNCTION FOR SIGN UP 
def signup(request):
    # checking if the user is already authenticated or not 
    if request.user.is_authenticated:
        # It means that the user is already authenticated so we are redirecting him to the home # page.            
        return HttpResponseRedirect(reverse('application:index'))
    
    # User is not authenticated 
    else:
        form = CreateUserForm()
        
        # if the user has submitted the form means the request method is post so collecting all the data from the client side in 'form_data' and populating our 'CreateUserForm' object 
        if request.method == "POST": 

            form_data = request.POST
            form = CreateUserForm(form_data)
            
            # checking, if the form is valid or not, if yes then saving it in the database 
            if form.is_valid():
                form.save()     # Saving all info in the DB

                # now after saving the form, collecting the username of the user from the form object to send it for the success message to the log in page. 
                user_name = form.cleaned_data.get('username')

                # making the account creation message and sending that message to the log in page 
                messages.success(request, f"Account for {user_name} has been made successfully, You can now log in")

                error = False

                # finally redirecting to the log in page with success message in it 
                return HttpResponseRedirect(reverse('application:login'), {'error':error})
            
            # if the form is not valid then rendering again the sign-up form with errors 
            else:
                return render(request, 'signup.html', {'form':form})
        
        # now if the user is requesting the signup page rather than submitting the info from the signp page i.e the request method is GET so just sending the empty form object to the sign up page .
        else:
            context = {'form':form}
            return render(request, 'signup.html', context)



# FUNCTION FOR LOG IN 
def log_in(request):
    
    # checking if the user is already authenticated or not 
    if request.user.is_authenticated:
        # It means that the user is already authenticated so we are redirecting him to the home # page.            
        return HttpResponseRedirect(reverse('application:index'))
    
    # User is not authenticated 
    else:
        # fetching the next parameter (the url to which the user is to be redirected after a successfull log in) for a GET Request 
        next_param = request.GET.get('next')

        # if the request is POST i.e the user enters username and password in order to log in 
        if request.method == "POST":
            # fetching the next parameter (the url to which the user is to be redirected after a successfull log in) for a POST Request. Also fetching the username and password for authenticating.

            next_param = request.POST.get('next')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Now authenticating the user by calling the 'auth.authenticate' method in a var called user 
            user = authenticate(request, username=username, password=password)

            # user's value is True if the user entered the right credentials and false otherwise 
            if user is not None:
                # it means user == True 
                login(request, user)
                print(user)
                
                # making up the url to which the user is redirected after a successful login 
                redirection_url = f"{reverse('application:index')}{next_param}"
                
                # checking if the next parameter is an empty string so in this case, redirecting the user to the home page 
                if next_param == "":
                    return HttpResponseRedirect(reverse('application:index'))
                else:
                    return HttpResponseRedirect(redirection_url)
            
            # if the user enters wrong credenials then 
            else:
                error = True
                messages.error(request, f"Incorrect Username or Password, Try Again.")
                context = {'error':error}
                return render(request, 'login.html', context)
        
        
        # if the request method is get means either the user has successfully make a new acccount or the user has entered the wrong credentials 
        else:
            context = {'error':False}
            return render(request, 'login.html', context)

# FUNCTION FOR LOG OUT 
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('application:index'))

from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render

from django.conf import settings


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from gnanow_project.settings import RAZORPAY_ID

# from gnanow_project.gnanow_project.settings import RAZORPAY_ID

# from gnanow_project.gnanow_project.settings import RAZORPAY_ID

def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user and clears all session data.

    Args:
        request: The HttpRequest object.

    Returns:
        A HttpResponse redirecting to a specified URL (e.g., homepage or login page).
    """
    # Log out the user from Django's authentication system
    # This removes the authenticated user's ID from the session and
    # clears any other authentication-related session data.
    logout(request)

    # Clear all data from the current session.
    # This ensures that any custom data stored in the session is also removed.
    # request.session.flush() will delete the session from the database
    # and create a new, empty session cookie.
    try:
        request.session.flush()
    except Exception as e:
        # Handle any potential exceptions during session flush, though rare.
        # You might want to log this error.
        print(f"Error flushing session: {e}")
        # Depending on your application's needs, you might still redirect
        # or show an error page. For simplicity, we'll still try to redirect.

    # After logging out and clearing the session, redirect the user.
    # It's common to redirect to the homepage or a login page.
    # Replace 'home' with the name of the URL pattern you want to redirect to.
    # If you don't have a 'home' URL, you can use '/' or another appropriate URL.
    return redirect('/login') # Or redirect('/') or redirect('login_page_name')

# Create your views here.
def landing_page1(request):
    return render(request, 'landing_page1.html')

def landing_page2(request):
    # Get the latest 10 products based on creation date
    recent_products = list(Product.objects.prefetch_related('variants__images').order_by('-created_at')[:10])
    
    # Shuffle to select 4 random recent ones
    random.shuffle(recent_products)
    selected_products = recent_products[:4]

    # Prepare structured data with variant + first image
    new_arrivals = []
    for product in selected_products:
        first_variant = product.variants.first()
        first_image = None

        if first_variant and first_variant.images.exists():
            first_image = first_variant.images.first().image.url

        new_arrivals.append({
            'product': product,
            'image_url': first_image,
            'price': first_variant.price if first_variant and first_variant.price else product.base_price
        })

   
    
    lookbook_dir = os.path.join(settings.STATICFILES_DIRS[0], 'lookbook')

    # List all image filenames in the directory
    all_images = [img for img in os.listdir(lookbook_dir) if img.startswith('lookbook') and img.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]

    # Shuffle and pick 5 random images
    random.shuffle(all_images)
    selected_images = all_images[:4]

    # Generate URLs for template
    lookbook_images = [f'lookbook/{img}' for img in selected_images]
    context = {
        'new_arrivals': new_arrivals,
        'lookbook_images':lookbook_images
    }
    return render(request, 'landing_page2.html', context)

    # return render(request, 'landing_page2.html')


import os
import random
from django.conf import settings
from django.shortcuts import render

# def home_view(request):
#     # Path to the lookbook folder
#     lookbook_dir = os.path.join(settings.STATICFILES_DIRS[0], 'lookbook')

#     # List all image filenames in the directory
#     all_images = [img for img in os.listdir(lookbook_dir) if img.startswith('lookbook') and img.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]

#     # Shuffle and pick 5 random images
#     random.shuffle(all_images)
#     selected_images = all_images[:5]

#     # Generate URLs for template
#     lookbook_images = [f'lookbook/{img}' for img in selected_images]

#     return render(request, 'landing_page2.html', {
#         'lookbook_images': lookbook_images,
#     })

def login(request):
    return render(request, 'loginpage.html')

def signup(request):
    return render(request, 'signup.html')



import base64

def encode_password(password):
    encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    return encoded_password




def decode_password(encoded_password):
    try:
        decoded_password = base64.b64decode(encoded_password).decode('utf-8')
    except UnicodeDecodeError:
        # Handle the case where decoding fails due to invalid characters
        decoded_password = "Unable to decode password"
    return decoded_password


import random
import string

def generate_random_word_and_append(username_string):
    """
    Generates a random 5-letter word and appends it to a given username string.

    Args:
        username_string (str): The original username string.

    Returns:
        str: The username string with a randomly generated 5-letter word appended.
    """
    # Get all lowercase English letters
    letters = string.ascii_lowercase

    # Generate a random 5-letter word
    # random.choice(letters) picks one random letter from the 'letters' string
    # The loop runs 5 times to pick 5 letters
    # ''.join(...) concatenates these 5 chosen letters into a single string
    random_word = ''.join(random.choice(letters) for i in range(5))

    # Append the randomly generated word to the original username string
    new_username = username_string + random_word
    return new_username

# --- Example Usage ---
# You can uncomment the lines below to test the function.

# Example 1: Appending to a base username
# original_username_1 = "user123_"
# updated_username_1 = generate_random_word_and_append(original_username_1)
# print(f"Original username 1: {original_username_1}")
# print(f"Updated username 1: {updated_username_1}")
# # Expected output: Original username 1: user123_
# #                  Updated username 1: user123_abcde (where 'abcde' is random)

# Example 2: Appending to another string
# original_username_2 = "guest"
# updated_username_2 = generate_random_word_and_append(original_username_2)
# print(f"\nOriginal username 2: {original_username_2}")
# print(f"Updated username 2: {updated_username_2}")
# # Expected output: Original username 2: guest
# #                  Updated username 2: guestfghij (where 'fghij' is random)

 
# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.tokens import default_token_generator
# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from .models import mainuser 
# def user_form_submit(request):
#     if request.method == 'POST':
#         user_name = request.POST['username']
#         print(user_name)
       
#         user_mail = request.POST['email']
#         user_password = request.POST['password']
#         user_dob = request.POST['dob']
#         user_phonenumber = request.POST['phone']
#         gender=request.POST['gender']
        
#         # en_password = encode_password(user_password)
#         en_password=encode_password(user_password)
#         print(user_password)
#         print(en_password)
#         fname=generate_random_word_and_append(user_name)
#         # Check if a user with the same email already exists
#         if mainuser.objects.filter(user_mail=user_mail).exists():
#             error_message = "A user with this email already exists. Please use a different email."
#             return render(request, 'signup.html', {'error_message': error_message})

#         # Create a new User instance
#         user = User.objects.create_user(username=fname, email=user_mail, password=user_password)
#         user.username = fname
#         user.is_active = False  # User is inactive until email confirmation
#         user.save()

#         # Create a new MainUser instance
#         new_user = mainuser(
          
#             username=user_name,
#             user_mail=user_mail,
#             user_password=en_password,
#             user_dob=user_dob,
#             user_gender=gender,
#             user_phonenumber=user_phonenumber
#         )
#         new_user.save()

#         # Send confirmation email
#         current_site = get_current_site(request)
#         mail_subject = 'Activate your account.'
#         message = render_to_string('acc_active_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#         })
#         # send_mail(mail_subject, message, 'settings.EMAIL_HOST_USER', [user_mail])
#         email_from = settings.EMAIL_HOST_USER
#             # subject = 'Feedback from User'
#         html_message = f"""
#             {message}
#             """
#         sendemail = EmailMessage(mail_subject, html_message, email_from, [user_mail])
#         sendemail.content_subtype = 'html'  # Set the content type to HTML
#         sendemail.send()
#         return render(request,'requestdone.html',{'user':new_user})
#         # return HttpResponse('Please confirm your email address to complete the registration')
#         # return render(request, 'acc_active_email.html', {'newuser': new_user})

#     else:
#         return render(request, 'signup.html')

# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return render(request, 'gotologin.html')
#         # return HttpResponse('Thank you for your email confirmation. Your account is now active. You can log in.')
#     else:
#         return HttpResponse('Activation link is invalid!')



from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage # Ensure EmailMessage is imported
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import CartItem, Wishlist, mainuser
from django.conf import settings # Import settings to access EMAIL_HOST_USER

# Assuming encode_password and generate_random_word_and_append are defined elsewhere.
# For a complete, runnable example, I'm including placeholder definitions.
# In your actual project, ensure these are correctly imported or defined.

# Placeholder for encode_password (replace with your actual encoding logic)


# Placeholder for generate_random_word_and_append (from your previous immersive)
import random
import string
def generate_random_word_and_append(username_string):
    """
    Generates a random 5-letter word and appends it to a given username string.
    """
    letters = string.ascii_lowercase
    random_word = ''.join(random.choice(letters) for i in range(5))
    new_username = username_string + random_word
    return new_username


def user_form_submit(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        print(f"User Name from form: {user_name}") # Debug print

        user_mail = request.POST['email']
        user_password = request.POST['password']
        user_dob = request.POST['dob']
        user_phonenumber = request.POST['phone']
        gender = request.POST['gender']

        en_password = encode_password(user_password)
        print(f"Original Password: {user_password}") # Debug print
        print(f"Encoded Password: {en_password}") # Debug print

        # Generate a unique username for the Django User model by appending a random word
        django_username = generate_random_word_and_append(user_name)
        print(f"Django User username (with random suffix): {django_username}") # Debug print

        # Check if a user with the same email already exists in your custom mainuser model
        if mainuser.objects.filter(user_mail=user_mail).exists():
            error_message = "A user with this email already exists. Please use a different email."
            return render(request, 'signup.html', {'error_message': error_message})

        # Create a new Django User instance
        # The 'username' field of Django's User model must be unique.
        user = User.objects.create_user(username=django_username, email=user_mail, password=user_password)
        user.is_active = False  # User is inactive until email confirmation
        user.save()

        # Create a new MainUser instance (your custom user profile)
        new_user = mainuser(
            username=user_name, # This stores the original username provided by the user
            user_mail=user_mail,
            user_password=en_password, # Store the encoded password here
            user_dob=user_dob,
            user_gender=gender,
            user_phonenumber=user_phonenumber
        )
        new_user.save()

        # Prepare and send confirmation email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        
        # Render the email content from a template
        message_body = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        email_from = settings.EMAIL_HOST_USER
        # The message_body is already an HTML string from render_to_string,
        # so no need for an f-string wrapper like `html_message = f"""{message}"""`
        html_content = message_body

        try:
            # Instantiate EmailMessage with explicit keyword arguments for clarity
            sendemail = EmailMessage(
                subject=mail_subject,
                body=html_content,
                from_email=email_from,
                to=[user_mail], # 'to' always expects a list of email addresses
            )
            sendemail.content_subtype = 'html'  # Crucial for rendering HTML content
            sendemail.send()
            print(f"Activation email sent successfully to {user_mail}") # Debug print
        except Exception as e:
            print(f"Error sending activation email to {user_mail}: {e}") # Debug print
            # Return an error message to the user if email sending fails
            return HttpResponse(f"There was an error sending the activation email. Please try again later. Error details: {e}")

        # Redirect to a page indicating successful registration and email sent
        return render(request,'requestdone.html',{'user':new_user})

    else:
        # If not a POST request, render the signup form
        return render(request, 'signup.html')

# def activate(request, uidb64, token):
#     """
#     View to activate a user account via email confirmation link.
#     """
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         # Optionally, you might want to log the user in here after activation
#         # from django.contrib.auth import login
#         # login(request, user)
#         return render(request, 'gotologin.html') # Redirect to a login success page
#     else:
#         return HttpResponse('Activation link is invalid!') # Inform user about invalid link
def remove_last_five_chars(input_string):
    """
    Removes the last 5 characters from a given string.

    Args:
        input_string (str): The string from which to remove characters.

    Returns:
        str: The string with the last 5 characters removed.
             Returns an empty string if the input_string has fewer than 5 characters.
    """
    # Check if the string is long enough to remove 5 characters
    if len(input_string) >= 5:
        # Use slicing to get all characters except the last 5
        return input_string[:-5]
    else:
        # If the string is too short, return an empty string
        # You could also choose to return the original string or raise an error
        return ""

# --- Example Usage ---
# original_username = "sknehduabcde"
# new_username = remove_last_five_chars(original_username)
# print(f"Original: '{original_username}'")
# print(f"Modified: '{new_username}'")

# print("-" * 20)

# # Example with a shorter string
# short_username = "user"
# new_short_username = remove_last_five_chars(short_username)
# print(f"Original: '{short_username}'")
# print(f"Modified: '{new_short_username}'")

# print("-" * 20)

# # Example with exactly 5 characters
# five_char_username = "hello"
# new_five_char_username = remove_last_five_chars(five_char_username)
# print(f"Original: '{five_char_username}'")
# print(f"Modified: '{new_five_char_username}'")



def get_last_five_chars(input_string):
    """
    Extracts and returns the last 5 characters from a given string.

    Args:
        input_string (str): The string from which to extract characters.

    Returns:
        str: The last 5 characters of the string.
             Returns the entire string if it has fewer than 5 characters.
    """
    # Use slicing to get the last 5 characters
    # If the string is shorter than 5, this slice will return the entire string
    return input_string[-5:]

# --- Example Usage ---
# original_username_1 = "sknehduabcde"
# last_five_1 = get_last_five_chars(original_username_1)
# print(f"Original: '{original_username_1}'")
# print(f"Last 5 chars: '{last_five_1}'")
# # Expected: Original: 'sknehduabcde', Last 5 chars: 'abcde'

# print("-" * 20)

# # Example with a shorter string (less than 5 characters)
# short_username = "user"
# last_five_2 = get_last_five_chars(short_username)
# print(f"Original: '{short_username}'")
# print(f"Last 5 chars: '{last_five_2}'")
# # Expected: Original: 'user', Last 5 chars: 'user'

# print("-" * 20)

# # Example with exactly 5 characters
# five_char_username = "hello"
# last_five_3 = get_last_five_chars(five_char_username)
# print(f"Original: '{five_char_username}'")
# print(f"Last 5 chars: '{last_five_3}'")
# # Expected: Original: 'hello', Last 5 chars: 'hello'


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("111111111111111111111111111111111")

    if user is not None and default_token_generator.check_token(user, token):
        print(" mnbkb")
        print("user= ",    user.username)
        a=user.username
        print("a==", a)
        u2=remove_last_five_chars(a)
        
        user.is_active = True
        user.save()
        user2= mainuser.objects.get(username=u2)
        if user2:
            user2.is_active=True
            user2.save()
            print("saved.....!!")
        print("debngdfddddddddddddddd")
        return render(request, 'gotologin.html')
        # return HttpResponse('Thank you for your email confirmation. Your account is now active. You can log in.')
    else:
        return HttpResponse('Activation link is invalid!')

def login_operation(request):
    error_message1 = None
    error_message2 = None
    
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_pass = request.POST.get('password')

        try:
            
            # Retrieve user based on email
            user = mainuser.objects.get(user_mail=user_email)
            if not user.is_active:
                error_message1 = "Account not activated. Please check your email."
                return render(request, 'loginpage.html', {'error_message1':error_message1 })


            encode_pass=encode_password(user_pass)
            # stored_password= base64.b64decode(user.user_password).decode('utf-8')
            # stored_password=decode_password(user.user_password)
            print(encode_pass)
            print(user_pass)
            print(user.user_password)
            if encode_pass == user.user_password:
                request.session['user_id'] = user.user_id
                # return redirect('home')
                success_message = "Successfully logged in."
                return redirect('dashboard')
                # return render(request, 'landing_page1.html',{'success_message': success_message, 'username':user.username})
            else:
                 error_message1 = "Invalid password."
                 return render(request, 'loginpage.html', {'error_message1': error_message1})
                
            # Check if the email and password match
            # if check_password(user_pass, user.user_password):
            #     # Authentication succeeds, store user ID in session and redirect to profile page
            #     request.session['user_id'] = user.user_id
            #     return redirect('home')
            # else:
                # Password does not match, render the login page with error message
                # error_message1 = "Invalid password."
                # return render(request, 'login.html', {'error_message1': error_message1})
          
        except mainuser.DoesNotExist:
            # User with provided email does not exist, render the login page with error message
            error_message2 = "User with this email does not exist."
            return render(request, 'loginpage.html', {'error_message2': error_message2})

    else:
        # GET request, render the login page
        return render(request, 'loginpage.html')




def about(request):
    return render(request, 'about.html')

def c_us(request):
    return render(request, 'contactus.html')

# def dashboard(request):
#     return render(request, 'dashboard.html')


from django.shortcuts import render
from .models import Category, Product, ProductVariant, ProductImage # Import all necessary models

from django.shortcuts import render
from .models import Category

from django.shortcuts import render
from .models import Category, Product, ProductImage, ProductVariant

# def dashboard(request):
#     # Top 3 categories
#     top_categories = Category.objects.all().order_by('-name')[:3]

#     # Fetch latest 4 products with at least one variant and image
#     featured_products = Product.objects.prefetch_related('variants__images').all().order_by('-created_at')[:4]

#     wishlist_variant_ids = []
#     user_id = request.session.get('user_id')
#     if user_id:
#         user = get_object_or_404(User, id=user_id)
#         wishlist_variant_ids = Wishlist.objects.filter(user=user).values_list('variant_id', flat=True)

#     context = {
#         'top_categories': top_categories,
#         'featured_products': featured_products,
#         'wishlist_variant_ids': list(wishlist_variant_ids),
#     }

#     return render(request, 'dashboard.html', context)
    # return render(request, 'dashboard.html')

# def dashboard(request):
#     top_categories = Category.objects.order_by('-name')[:3]
#     products = Product.objects.all().order_by('-created_at')[:4]

#     user_id = request.session.get('user_id')
#     wishlist_variant_ids = []
#     if user_id:
#         user = get_object_or_404(mainuser, user_id=user_id)
#         wishlist_variant_ids = Wishlist.objects.filter(user=user).values_list('variant_id', flat=True)

#     context = {
#         'top_categories': top_categories,
#         'products': products,
#         'wishlist_variant_ids': list(wishlist_variant_ids),
#     }
#     return render(request, 'dashboard.html', context)



from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import mainuser
from django.contrib.auth.decorators import login_required

# @login_required
def profile(request):
    # Retrieve the logged-in user based on session data
    user_id = request.session.get('user_id')
    if user_id:
        user = mainuser.objects.get(user_id=user_id)
        return render(request, 'profile.html', {'user': user})
    else:
        # Redirect to login page if user is not logged in
        return redirect('login')
    


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gnanow.models import mainuser
from django.contrib import messages

# @login_required
def edit_profile(request):
    try:
        user = mainuser.objects.get(user_id=request.session.get('user_id'))
    except mainuser.DoesNotExist:
        return redirect('login')  # Redirect if the mainuser profile does not exist

    if request.method == 'POST':
        user.username = request.POST.get('user_name')
        user.user_dob = request.POST.get('user_dob')
        user.user_phonenumber = request.POST.get('user_phonenumber')
        user.user_gender=request.POST.get('user_gender')

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Redirect to the profile view after saving

    return render(request, 'edit_userprofile.html', {'user': user})



from django.shortcuts import render
from .models import Product

import random
from django.shortcuts import render
from .models import Product
import random

# def home_view(request):
    
    

# def add_to_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, "Please log in to use the wishlist.")
#         return redirect('login')

#     user = get_object_or_404(User, id=user_id)
#     variant = get_object_or_404(ProductVariant, id=variant_id)

#     wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
#     if created:
#         messages.success(request, "Variant added to wishlist.")
#     else:
#         messages.info(request, "Variant already in wishlist.")
#     return redirect('dashboard')


# def remove_from_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, "Please log in to use the wishlist.")
#         return redirect('login')

#     user = get_object_or_404(User, id=user_id)
#     Wishlist.objects.filter(user=user, variant_id=variant_id).delete()
#     messages.success(request, "Variant removed from wishlist.")
#     return redirect('wishlist')


from django.shortcuts import redirect
# from .models import ProductVariant, Wishlist

# def add_to_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if user_id:
#         variant = get_object_or_404(ProductVariant, id=variant_id)
#         Wishlist.objects.get_or_create(user_id=user_id, variant=variant)
#     return redirect('dashboard')

# def remove_from_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if user_id:
#         Wishlist.objects.filter(user_id=user_id, variant_id=variant_id).delete()
#     return redirect('dashboard')



# def dashboard(request):
#     top_categories = Category.objects.all().order_by('-name')[:3]
#     featured_products = Product.objects.prefetch_related('variants__images').order_by('-created_at')[:4]

#     wishlist_variant_ids = []
#     user_id = request.session.get('user_id')
#     if user_id:
#         user = get_object_or_404(User, id=user_id)
#         wishlist_variant_ids = Wishlist.objects.filter(user=user).values_list('variant_id', flat=True)

#     context = {
#         'top_categories': top_categories,
#         'featured_products': featured_products,
#         'wishlist_variant_ids': list(wishlist_variant_ids),
#     }

#     return render(request, 'dashboard.html', context)


# def add_to_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if user_id:
#         variant = get_object_or_404(ProductVariant, id=variant_id)
#         Wishlist.objects.get_or_create(user_id=user_id, variant=variant)
#     return redirect('dashboard')

# def remove_from_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if user_id:
#         Wishlist.objects.filter(user_id=user_id, variant_id=variant_id).delete()
#     return redirect('dashboard')



# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, Product, ProductVariant, Category, User

# def dashboard(request):
#     top_categories = Category.objects.all().order_by('-name')[:3]
#     featured_products = Product.objects.prefetch_related('variants__images').order_by('-created_at')[:4]

#     wishlist_variant_ids = []
#     user_id = request.session.get('user_id')
#     if user_id:
#         user = get_object_or_404(User, id=user_id)
#         wishlist_variant_ids = Wishlist.objects.filter(user=user).values_list('variant_id', flat=True)

#     context = {
#         'top_categories': top_categories,
#         'featured_products': featured_products,
#         'wishlist_variant_ids': list(wishlist_variant_ids),
#     }

#     return render(request, 'dashboard.html', context)






# def dashboard(request):
#     top_categories = Category.objects.all().order_by('-name')[:3]
#     featured_products = Product.objects.prefetch_related('variants__images').order_by('-created_at')[:4]
#     status=""
#     wishlist_variant_ids = []
#     wishlist_count = 0
#     user_id = request.session.get('user_id')

#     if user_id:
#         user = get_object_or_404(mainuser, user_id=user_id)
#         wishlist_items = Wishlist.objects.filter(user=user)
#         wishlist_variant_ids = wishlist_items.values_list('variant_id', flat=True)
#         wishlist_count = wishlist_items.count()
#         if request.GET.get('status'):
#             status=request.GET.get('status')
#         else:
#             status = "-1"
            
        

#         context = {
#             'top_categories': top_categories,
#             'featured_products': featured_products,
#             'wishlist_variant_ids': list(wishlist_variant_ids),
#             'wishlist_count': wishlist_count,  # 🆕 Send count to template
#             'status':status,
#         }
        

#         return render(request, 'dashboard.html', context)
#     else:
#         return redirect('login')



def dashboard(request):
    top_categories = Category.objects.all().order_by('-name')[:3]
    featured_products = Product.objects.prefetch_related('variants__images').order_by('-created_at')[:4]
    status = ""
    wishlist_variant_ids = []
    wishlist_count = 0
    cart_count=0

    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(mainuser, user_id=user_id)
        wishlist_items = Wishlist.objects.filter(user=user)
        cart_items=CartItem.objects.filter(user=user)
        wishlist_variant_ids = wishlist_items.values_list('variant_id', flat=True)
        wishlist_count = wishlist_items.count()
        cart_count=cart_items.count()
        status = request.GET.get('status', "-1")

        # Add stock info to each product
        for product in featured_products:
            first_variant = product.variants.first()
            product.first_variant = first_variant
            product.variant_stock = first_variant.stock if first_variant else 0

        context = {
            'top_categories': top_categories,
            'featured_products': featured_products,
            'wishlist_variant_ids': list(wishlist_variant_ids),
            'wishlist_count': wishlist_count,
            'status': status,
            'cart_count':cart_count,
        }

        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')


# def toggle_wishlist(request, variant_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')  # or handle unauthenticated users
#     user = get_object_or_404(mainuser, user_id=user_id)
#     variant = get_object_or_404(ProductVariant, id=variant_id)

#     wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
#     if not created:
#         wishlist_item.delete()

#     return redirect('wishlist')







from django.contrib.auth.decorators import login_required

# def wishlist_view(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')  # Adjust if you're using custom login

#     user = get_object_or_404(mainuser, user_id=user_id)
#     wishlist_items = Wishlist.objects.select_related('variant__product').filter(user=user)

#     context = {
#         'wishlist_items': wishlist_items
#     }
#     return render(request, 'wishlist.html', context)



def toggle_wishlist_dashboard(request, variant_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # or handle unauthenticated users
    user = get_object_or_404(mainuser, user_id=user_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
    if not created:
        wishlist_item.delete()
        return HttpResponseRedirect(reverse('dashboard') + '?status=0')  # Removed
    else:
        return HttpResponseRedirect(reverse('dashboard') + '?status=1')  # Added





def toggle_wishlist_p_list(request, variant_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # or handle unauthenticated users
    user = get_object_or_404(mainuser, user_id=user_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
    if not created:
        wishlist_item.delete()
        return HttpResponseRedirect(reverse('product_list') + '?status=0')  # Removed
    else:
        return HttpResponseRedirect(reverse('product_list') + '?status=1')  # Added



# def toggle_wishlist_p_details(request, variant_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')  # or handle unauthenticated users
#     user = get_object_or_404(mainuser, user_id=user_id)
#     variant = get_object_or_404(ProductVariant, id=variant_id)

#     wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
#     if not created:
#         wishlist_item.delete()
#         return HttpResponseRedirect(reverse('product_detail') + '?status=0')  # Removed
#     else:
#         return HttpResponseRedirect(reverse('product_detail') + '?status=1')  # Added



from django.http import HttpResponseRedirect
from django.urls import reverse

def toggle_wishlist_p_details(request, variant_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # or handle unauthenticated users

    user = get_object_or_404(mainuser, user_id=user_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_slug = variant.product.slug  # ✅ Get the product's slug for redirection

    wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
    if not created:
        wishlist_item.delete()
        return HttpResponseRedirect(reverse('product_detail', kwargs={'slug': product_slug}) + '?status=0')
    else:
        return HttpResponseRedirect(reverse('product_detail', kwargs={'slug': product_slug}) + '?status=1')

    # if not created:
    #     wishlist_item.delete()
    
    # return redirect('dashboard')


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def toggle_wishlist(request, variant_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(mainuser, user_id=user_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    wishlist_item, created = Wishlist.objects.get_or_create(user=user, variant=variant)
    if not created:
        wishlist_item.delete()
        return HttpResponseRedirect(reverse('wishlist') + '?status=0')  # Removed
    else:
        return HttpResponseRedirect(reverse('wishlist') + '?status=1')  # Added


from django.shortcuts import render, get_object_or_404, redirect
from .models import Wishlist, mainuser

def wishlist_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(mainuser, user_id=user_id)
    wishlist_items = Wishlist.objects.select_related('variant__product').filter(user=user)

    status = request.GET.get('status')  # Get '1' or '0' from URL
    print("status===",status)
    context = {
        'wishlist_items': wishlist_items,
        'status': status
    }
    return render(request, 'wishlist.html', context)




from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

# def add_to_cart(request, variant_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, "Login required to add to cart.")
#         return redirect('login')

#     variant = get_object_or_404(ProductVariant, id=variant_id)
#     cart_item, created = CartItem.objects.get_or_create(user_id=user_id, variant=variant)
    
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('dashboard')


# views.py
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@require_POST
def add_to_cart(request, variant_id):
    user_id = request.session.get('user_id')
    quantity = int(request.POST.get('quantity', 1))

    if not user_id:
        return redirect('login')  # or handle guest cart

    # You should create or update cart logic here
    # Example:
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart_item, created = CartItem.objects.get_or_create(user_id=user_id, variant=variant)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('view_cart')  # or wherever you want



# def remove_from_cart(request, item_id):
#     user_id = request.session.get('user_id')
#     CartItem.objects.filter(id=item_id, user_id=user_id).delete()
#     return redirect('view_cart')



from django.shortcuts import get_object_or_404, redirect
from .models import CartItem

def remove_from_cart(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # optional

    cart_item = get_object_or_404(CartItem, id=item_id, user_id=user_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')

# def view_cart(request):
#     user_id = request.session.get('user_id')
#     cart_items = CartItem.objects.filter(user_id=user_id).select_related('variant__product')
#     total = sum(item.variant.price * item.quantity for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total': total,
#     }
#     return render(request, 'cart.html', context)

def view_cart(request):
    # user_id = request.session.get('user_id')
    user_id = request.session.get('user_id')
    if user_id:
        user = mainuser.objects.get(user_id=user_id)
    else:
        # Redirect to login page if user is not logged in
        return redirect('login')
    if not user:
        return redirect('login')
    cart_items = CartItem.objects.filter(user_id=user_id).select_related('variant__product')

    subtotal = 0
    for item in cart_items:
        item.total_price = item.variant.price * item.quantity
        subtotal += item.total_price

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': subtotal,  # Add shipping or tax later if needed
    }
    return render(request, 'cart.html', context)


from django.shortcuts import get_object_or_404, redirect
from .models import CartItem

def increase_cart_quantity(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # optional

    cart_item = get_object_or_404(CartItem, id=item_id, user_id=user_id)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart')




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Address
from django.contrib.auth.decorators import login_required

def my_addresses(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Or wherever you handle authentication

    addresses = Address.objects.filter(user_id=user_id).order_by('-is_default', '-created_at')
    return render(request, 'myaddress.html', {'addresses': addresses})




def edit_address(request, address_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    address = get_object_or_404(Address, id=address_id, user_id=user_id)

    if request.method == 'POST':
        address.address_line1 = request.POST.get('address_line1')
        address.address_line2 = request.POST.get('address_line2')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.postal_code = request.POST.get('postal_code')
        address.country = request.POST.get('country')
        address.phone_number=request.POST.get('phone')
        is_default = request.POST.get('is_default') == 'on'

        if is_default:
            Address.objects.filter(user_id=user_id, is_default=True).exclude(id=address.id).update(is_default=False)

        address.is_default = is_default
        address.save()
        return redirect('my_addresses')

    return render(request, 'edit_address.html', {'address': address})


def delete_address(request, address_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    address = get_object_or_404(Address, id=address_id, user_id=user_id)
    address.delete()
    return redirect('my_addresses')


def add_address(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        address = Address(
            user_id=user_id,
            address_line1=request.POST.get('address_line1'),
            address_line2=request.POST.get('address_line2'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            phone_number=request.POST.get('phone'),
            is_default=request.POST.get('is_default') == 'on'
        )

        if address.is_default:
            Address.objects.filter(user_id=user_id, is_default=True).update(is_default=False)

        address.save()
        return redirect('my_addresses')

    return render(request, 'add_address.html')



def add_address_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        address = Address(
            user_id=user_id,
            address_line1=request.POST.get('address_line1'),
            address_line2=request.POST.get('address_line2'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            phone_number=request.POST.get('phone'),
            is_default=request.POST.get('is_default') == 'on'
        )

        if address.is_default:
            Address.objects.filter(user_id=user_id, is_default=True).update(is_default=False)

        address.save()
        return redirect('placeorder')

    return render(request, 'add_address.html')

# def placeorder(request):
    
#     return render(request, 'placeorder.html')
from django.shortcuts import render, redirect
from .models import Address

def placeorder(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # or show an error

    addresses = Address.objects.filter(user_id=user_id)

    return render(request, 'placeorder.html', {'addresses': addresses})



# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from .models import CartItem, Order, OrderItem, Address, Product

# def create_order(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')  # or show an error
    
#     address_id = request.POST.get('address_id')
#     if not address_id:
#         return redirect('placeorder')  # or show an error

#     cart_items = CartItem.objects.filter(user_id=user_id)
#     if not cart_items.exists():
#         return redirect('view_cart')  # or show message: cart is empty

#     address = Address.objects.get(id=address_id, user_id=user_id)

#     # Calculate total
#     total_amount = 0
#     for item in cart_items:
#         total_amount += item.variant.price * item.quantity

#     # Create Order
#     order = Order.objects.create(
#         user_id=user_id, 
#         address=address,
#         total_amount=total_amount,
#         status='Pending'
#     )
#     # print("order_id ==", order.order_id)

#     # Create Order Items
#     for item in cart_items:
#         OrderItem.objects.create(
#             order=order,
#             product=item.variant.product,
#             quantity=item.quantity,
#             price=item.variant.price
#         )
#     # Clear cart
#     cart_items.delete()

#     return render(request,'payment.html', {'order_id': order.order_id})


# from django.shortcuts import render, redirect, get_object_or_404
# from .models import CartItem, Order, OrderItem, Address

# def create_order(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')

#     address_id = request.POST.get('address_id')
#     if not address_id:
#         return redirect('placeorder')

#     cart_items = CartItem.objects.select_related('variant__product').filter(user_id=user_id)
#     if not cart_items.exists():
#         return redirect('view_cart')

#     address = get_object_or_404(Address, id=address_id, user_id=user_id)

#     total_amount = sum(item.variant.price * item.quantity for item in cart_items)

#     # Create Order
#     order = Order.objects.create(
#         user_id=user_id,
#         address=address,
#         total_amount=total_amount,
#         status='Pending'
#     )

#     # Create Order Items
#     for item in cart_items:
#         OrderItem.objects.create(
#             order=order,
#             product=item.variant.product,
#             variant=item.variant,  # Store variant here
#             quantity=item.quantity,
#             price=item.variant.price
#         )

#     # Clear cart
#     cart_items.delete()

#     return render(request, 'payment.html', {'order_id': order.order_id})


from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Order, OrderItem, Address, ProductVariant

def create_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    address_id = request.POST.get('address_id')
    if not address_id:
        return redirect('placeorder')

    cart_items = CartItem.objects.select_related('variant__product').filter(user_id=user_id)
    if not cart_items.exists():
        return redirect('view_cart')

    address = get_object_or_404(Address, id=address_id, user_id=user_id)

    total_amount = sum(item.variant.price * item.quantity for item in cart_items)

    # Create Order
    order = Order.objects.create(
        user_id=user_id,
        address=address,
        total_amount=total_amount,
        status='Pending'
    )

    # Create Order Items and update stock
    for item in cart_items:
        variant = item.variant

        # Ensure enough stock is available
        if variant.stock < item.quantity:
            # Optional: delete the order if needed, or skip this item
            order.delete()
            return render(request, 'myorder.html', {
                'message': f"Not enough stock for {variant.product.name} - {variant.color} - {variant.size}"
            })

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=variant.product,
            variant=variant,
            quantity=item.quantity,
            price=variant.price
        )

        # Deduct stock
        variant.stock -= item.quantity
        variant.save()

    # Clear cart
    cart_items.delete()

    return render(request, 'payment.html', {'order_id': order.order_id})

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Order, Payment, mainuser

# razorpay_client = RAZORPAY_ID.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_ACCOUNT_ID))

def process_payment(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        user = mainuser.objects.get(user_id=user_id)
        order_id = request.POST.get("order_id")
        payment_method = request.POST.get("payment_method")
        order = Order.objects.get(order_id=order_id, user=user)
        user_id = request.session.get('user_id')
        if not user:
            # Redirect to login page if user is not logged in
            return redirect('login')

        if payment_method == "COD":
            Payment.objects.create(
                user=user,
                order=order,
                amount=order.total_amount,
                method="COD",
                status="Success"
            )
            order.status = "Processing"
            order.save()
            return redirect("order_success")

        elif payment_method == "Razorpay":
            razorpay_order = razorpay_client.order.create({
                "amount": int(order.total_amount * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            payment = Payment.objects.create(
                user=user,
                order=order,
                amount=order.total_amount,
                method="Razorpay",
                status="Pending",
                razorpay_order_id=razorpay_order['id']
            )

            context = {
                "order": order,
                "payment": payment,
                "razorpay_key_id": settings.RAZORPAY_ID,
                "razorpay_order_id": razorpay_order["id"],
                "amount": int(order.total_amount * 100),
                "currency": "INR",
                "callback_url": request.build_absolute_uri("/payment/verify/")
            }
            return render(request, "razorpay_checkout.html", context)

    return redirect("cart")



@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            payment.status = "Success"
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.save()

            order = payment.order
            order.status = "Processing"
            order.save()

            return redirect("order_success")

        except razorpay.errors.SignatureVerificationError:
            payment.status = "Failed"
            payment.save()
            return redirect("order_failed")

    return redirect("cart")


def order_failed(request):
    return render(request, 'order_failed.html')

def order_success(request):
    return render(request, 'order_success.html')



from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import mainuser
from .tokens import account_activation_token
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = mainuser.objects.get(user_mail=email)
            if not user:
                return redirect('login')
            signer = TimestampSigner()
            token = signer.sign(account_activation_token.make_token(user))
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            mail_subject = 'Reset your password'
            message = f"""\
            <html>
            <body>
            <p>Hi { user.username }</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_link }">{ reset_link }</a></p>
            </body>
            </html>
            """
            emailm = EmailMessage(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            emailm.content_subtype = 'html'
            emailm.send(fail_silently=False)
            return redirect('password_reset_done')
        except mainuser.DoesNotExist:
            return render(request, "password_reset_form.html", {'error': 'Email does not exist'})
    return render(request, "password_reset_form.html")


def password_reset_done(request):
    return render(request, "password_reset_done.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = mainuser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, mainuser.DoesNotExist):
        user = None
    
    if user is not None:
        signer = TimestampSigner()
        try:
            # Check if token is valid and not expired (2-minute limit)
            original_token = signer.unsign(token, max_age=300)  # 120 seconds = 2 minutes
            if account_activation_token.check_token(user, original_token):
                if request.method == "POST":
                    new_password = request.POST.get("new_password")
                    enpass=encode_password(new_password)
                    user.user_password = enpass  # Hash the password before saving
                    user.save()
                    return redirect('password_reset_complete')
                return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        except (SignatureExpired, BadSignature):
            return redirect('password_reset_invalid')
    return redirect('password_reset_invalid')

def password_reset_complete(request):
    return render(request, "password_reset_complete.html")

def password_reset_invalid(request):
    return render(request, "password_reset_invalid.html")



# from django.shortcuts import render, get_object_or_404
# from .models import Product, Category

# def product_list(request):
#     query = request.GET.get('query')
#     category_id = request.GET.get('category')

#     products = Product.objects.all()
#     categories = Category.objects.all()
#     related_products = None

#     if query:
#         products = products.filter(name__icontains=query)

#     if category_id:
#         products = products.filter(category_id=category_id)

#     if products.exists():
#         first_product = products.first()
#         related_products = Product.objects.filter(category=first_product.category).exclude(id=first_product.id)[:4]

#     return render(request, 'product_list.html', {
#         'products': products,
#         'categories': categories,
#         'query': query,
#         'related_products': related_products
#     })


# from django.shortcuts import render
# from .models import Product, Category

# def product_list(request):
#     query = request.GET.get('q', '')
#     category_id = request.GET.get('category')
#     color = request.GET.get('color')
#     size = request.GET.get('size')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     products = Product.objects.all()

#     if category_id:
#         products = products.filter(category__id=category_id)
#     if color:
#         products = products.filter(variants__color__iexact=color).distinct()
#     if size:
#         products = products.filter(variants__size__iexact=size).distinct()
#     if min_price:
#         products = products.filter(base_price__gte=min_price)
#     if max_price:
#         products = products.filter(base_price__lte=max_price)

#     matched_products = products
#     related_products = []

#     if query:
#         matched_products = products.filter(name__icontains=query)
#         if matched_products.exists():
#             related_products = Product.objects.filter(category=matched_products.first().category).exclude(id__in=matched_products.values_list('id', flat=True))[:8]

#     categories = Category.objects.all()
#     colors = Product.objects.values_list('variants__color', flat=True).distinct()
#     sizes = Product.objects.values_list('variants__size', flat=True).distinct()

#     return render(request, 'product_list.html', {
#         'matched_products': matched_products,
#         'related_products': related_products,
#         'categories': categories,
#         'colors': colors,
#         'sizes': sizes
#     })
from django.shortcuts import render
from django.db.models import Q, Min, Max
from .models import Product, ProductVariant, ProductImage, Category

# def product_list(request):
#     query = request.GET.get('q', '')
#     category = request.GET.get('category')
#     color = request.GET.get('color')
#     size = request.GET.get('size')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     products = Product.objects.all()

#     if query:
#         products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
#         if products.exists():
#             first_product = products.first()
#             related_products = Product.objects.filter(category=first_product.category).exclude(id=first_product.id)
#         else:
#             related_products = None
#     else:
#         related_products = None

#     # Filter by category
#     if category:
#         products = products.filter(category__slug=category)

#     # Filter by variant attributes
#     variant_ids = ProductVariant.objects.all()

#     if color:
#         variant_ids = variant_ids.filter(color=color)
    

#     if size:
#         variant_ids = variant_ids.filter(size=size)
   

#     if min_price:
#         variant_ids = variant_ids.filter(price__gte=min_price)
  
        

#     if max_price:
#         variant_ids = variant_ids.filter(price__lte=max_price)
 
#     # Filter product list based on variants
#     if color or size or min_price or max_price:
#         products = products.filter(variants__in=variant_ids).distinct()

#     categories = Category.objects.all()
#     colors = ProductVariant.COLOR_CHOICES
#     sizes = ProductVariant.SIZE_CHOICES

#     # For price range slider UI
#     price_range = ProductVariant.objects.aggregate(
#         min_price=Min('price'),
#         max_price=Max('price')
#     )

#     context = {
#         'products': products,
#         'categories': categories,
#         'colors': colors,
#         'sizes': sizes,
#         'query': query,
#         'related_products': related_products,
#         'price_range': price_range,
#     }
#     return render(request, 'product_list.html', context)



# from django.shortcuts import render
# from django.db.models import Q, Min, Max
# from .models import Product, ProductVariant, ProductImage, Category

# def product_list(request):
#     query = request.GET.get('q', '')
#     selected_categories = request.GET.getlist('category')  # ✅ Multi-select categories
#     selected_colors = request.GET.getlist('color')         # ✅ Multi-select colors
#     selected_sizes = request.GET.getlist('size')           # ✅ Multi-select sizes
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     products = Product.objects.all()

#     # Text search
#     if query:
#         products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
#         if products.exists():
#             first_product = products.first()
#             related_products = Product.objects.filter(category=first_product.category).exclude(id=first_product.id)
#         else:
#             related_products = None
#     else:
#         related_products = None

#     # Filter by selected categories
#     if selected_categories:
#         products = products.filter(category__slug__in=selected_categories)

#     # Variant filters
#     variant_filter = ProductVariant.objects.all()

#     if selected_colors:
#         variant_filter = variant_filter.filter(color__in=selected_colors)

#     if selected_sizes:
#         variant_filter = variant_filter.filter(size__in=selected_sizes)

#     if min_price:
#         variant_filter = variant_filter.filter(price__gte=min_price)

#     if max_price:
#         variant_filter = variant_filter.filter(price__lte=max_price)

#     # Apply variant-based product filter
#     if selected_colors or selected_sizes or min_price or max_price:
#         products = products.filter(variants__in=variant_filter).distinct()

#     # Metadata
#     categories = Category.objects.all()
#     colors = ProductVariant.COLOR_CHOICES
#     sizes = ProductVariant.SIZE_CHOICES
#     price_range = ProductVariant.objects.aggregate(min_price=Min('price'), max_price=Max('price'))

#     context = {
#         'products': products,
#         'categories': categories,
#         'colors': colors,
#         'sizes': sizes,
#         'query': query,
#         'related_products': related_products,
#         'selected_categories': selected_categories,
#         'selected_colors': selected_colors,
#         'selected_sizes': selected_sizes,
#         'price_range': price_range,
#     }

#     return render(request, 'product_list.html', context)



from django.shortcuts import render
from django.db.models import Q, Min, Max
from .models import Product, ProductVariant, Category, Wishlist

def product_list(request):
    query = request.GET.get('q', '')
    selected_categories = request.GET.getlist('category')
    selected_colors = request.GET.getlist('color')
    selected_sizes = request.GET.getlist('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    status=""
    products = Product.objects.all()
    
    

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if products.exists():
            first_product = products.first()
            related_products = Product.objects.filter(category=first_product.category).exclude(id=first_product.id)
        else:
            related_products = None
    else:
        related_products = None

    if selected_categories:
        products = products.filter(category__slug__in=selected_categories)

    variant_filter = ProductVariant.objects.all()

    if selected_colors:
        variant_filter = variant_filter.filter(color__in=selected_colors)

    if selected_sizes:
        variant_filter = variant_filter.filter(size__in=selected_sizes)

    if min_price:
        variant_filter = variant_filter.filter(price__gte=min_price)

    if max_price:
        variant_filter = variant_filter.filter(price__lte=max_price)

    if selected_colors or selected_sizes or min_price or max_price:
        products = products.filter(variants__in=variant_filter).distinct()

    categories = Category.objects.all()
    colors = ProductVariant.COLOR_CHOICES
    sizes = ProductVariant.SIZE_CHOICES
    price_range = ProductVariant.objects.aggregate(min_price=Min('price'), max_price=Max('price'))

    wishlist_variant_ids = []
    user_id = request.session.get('user_id')
    user = mainuser.objects.get(user_id=user_id)
    if user:
        if request.GET.get('status'):
            status=request.GET.get('status')
        else:
            status = "-1"
        wishlist_variant_ids = Wishlist.objects.filter(user=user).values_list('variant__id', flat=True)
    else:
        return redirect('login')

    context = {
        'products': products,
        'categories': categories,
        'colors': colors,
        'sizes': sizes,
        'query': query,
        'related_products': related_products,
        'selected_categories': selected_categories,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'price_range': price_range,
        'min_price': min_price,
        'max_price': max_price,
        'wishlist_variant_ids': wishlist_variant_ids,
        'status':status,
    }

    return render(request, 'product_list.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Product, ProductVariant, ProductImage

# def product_detail(request, slug):
#     status=""
#     user_id = request.session.get('user_id')
#     user = mainuser.objects.get(user_id=user_id)
#     if user:
#         if request.GET.get('status'):
#             status=request.GET.get('status')
#         else:
#             status = "-1"
#     else:
#         return redirect('login')
#     product = get_object_or_404(Product, slug=slug)

#     # Get all variants and images
#     variants = product.variants.all()
#     first_variant = variants.first()
#     images = ProductImage.objects.filter(variant__product=product)

#     # Related products from same category, excluding the current one
#     related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
#     # related_products_v=related_products.variants.all()
#     context = {
#         'product': product,
#         'variants': variants,
#         'first_variant': first_variant,
#         'images': images,
#         'related_products': related_products,
#         'status':status
#         # 'related_products_v':related_products_v,
#     }

#     return render(request, 'product_detail.html', context)



# def product_detail(request, slug):
#     status = ""
#     user_id = request.session.get('user_id')
#     user = mainuser.objects.filter(user_id=user_id).first()

#     if not user:
#         return redirect('login')

#     status = request.GET.get('status', "-1")

#     product = get_object_or_404(Product, slug=slug)
#     variants = product.variants.all()

#     # Get selected variant from GET or fallback to first
#     selected_variant_id = request.GET.get('variant_id')
#     if selected_variant_id:
#         first_variant = ProductVariant.objects.filter(id=selected_variant_id, product=product).first()
#     else:
#         first_variant = variants.first()
    
#     if selected_variant_id:
#         first_variant = ProductVariant.objects.filter(id=selected_variant_id, product=product).first()
#         images = ProductImage.objects.filter(variant=first_variant)  # 🆕 Specific variant images
#     else:
#         first_variant = variants.first()
#         images = ProductImage.objects.filter(variant__product=product)  # fallback


#     images = ProductImage.objects.filter(variant__product=product)
#     related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]

#     # ✅ Convert variants to JSON-safe format for JS
#     variant_json = json.dumps(list(variants.values('id', 'color', 'size')), cls=DjangoJSONEncoder)

#     context = {
#         'product': product,
#         'variants': variants,
#         'first_variant': first_variant,
#         'images': images,
#         'related_products': related_products,
#         'status': status,
#         'variant_json': variant_json  # ✅ Add here
#     }

#     return render(request, 'product_detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, ProductImage, mainuser
import json
from django.core.serializers.json import DjangoJSONEncoder

def product_detail(request, slug):
    status = ""
    user_id = request.session.get('user_id')
    user = mainuser.objects.filter(user_id=user_id).first()

    if not user:
        return redirect('login')

    status = request.GET.get('status', "-1")
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all()

    # Unique colors and sizes for dropdowns
    colors = list(set(v.color for v in variants))
    sizes = list(set(v.size for v in variants))

    selected_variant_id = request.GET.get('variant_id')
    if selected_variant_id:
        first_variant = ProductVariant.objects.filter(id=selected_variant_id, product=product).first()
    else:
        first_variant = variants.first()

    # Filter images for selected variant
    images = ProductImage.objects.filter(variant=first_variant) if first_variant else []

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    variant_json = json.dumps(list(variants.values('id', 'color', 'size')), cls=DjangoJSONEncoder)

    context = {
        'product': product,
        'variants': variants,
        'first_variant': first_variant,
        'colors': colors,
        'sizes': sizes,
        'images': images,
        'related_products': related_products,
        'status': status,
        'variant_json': variant_json,
    }

    return render(request, 'product_detail.html', context)


# from django.shortcuts import render
# from .models import Order

# def my_orders(request):
#     user_id = request.session.get('user_id')
#     user = mainuser.objects.get(user_id=user_id)
#     orders = Order.objects.filter(user=user).select_related('payment').prefetch_related('items__product')

#     # Filters
#     status = request.GET.get('status')
#     payment_status = request.GET.get('payment_status')
#     method = request.GET.get('method')

#     if status:
#         orders = orders.filter(status=status)
#     if payment_status:
#         orders = orders.filter(payment__status=payment_status)
#     if method:
#         orders = orders.filter(payment__method=method)

#     return render(request, 'myorder.html', {'orders': orders})



from django.shortcuts import render
from .models import Category

def categories_view(request):
    
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def feedback(request):
    return render(request, 'feedback.html')



# def my_orders(request):
#     user_id = request.session.get('user_id')
#     user = mainuser.objects.get(user_id=user_id)
#     orders = Order.objects.filter(user=user).select_related('payment').prefetch_related('items__product')

#     # Filters
#     status = request.GET.get('status')
#     payment_status = request.GET.get('payment_status')
#     method = request.GET.get('method')

#     if status:
#         orders = orders.filter(status=status)
#     if payment_status:
#         orders = orders.filter(payment__status=payment_status)
#     if method:
#         orders = orders.filter(payment__method=method)

#     context = {
#         'orders': orders,
#         'status_choices': ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'],
#         'payment_status_choices': ['Pending', 'Success', 'Failed'],
#         'method_choices': ['Razorpay', 'COD', 'Stripe'],
#     }
#     return render(request, 'myorder.html', context)



def my_orders(request):
    user_id = request.session.get('user_id')
    user = mainuser.objects.get(user_id=user_id)
    if not user:
        return redirect('login')
    
    # Get all orders for the user, newest first
    orders = Order.objects.filter(user=user)\
        .select_related('payment')\
        .prefetch_related('items__product')\
        .order_by('-created_at')  # 🔥 Order by newest first

    # Filters
    status = request.GET.get('status')
    payment_status = request.GET.get('payment_status')
    method = request.GET.get('method')

    if status:
        orders = orders.filter(status=status)
    if payment_status:
        orders = orders.filter(payment__status=payment_status)
    if method:
        orders = orders.filter(payment__method=method)

    context = {
        'orders': orders,
        'status_choices': ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'],
        'payment_status_choices': ['Pending', 'Success', 'Failed'],
        'method_choices': ['Razorpay', 'COD', 'Stripe'],
    }
    return render(request, 'myorder.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem, ProductImage

# def order_items_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_items = order.items.select_related('product', 'variant').all()

#     # For each item, get first image for the variant
#     for item in order_items:
#         item.image_url = None
#         if item.variant:
#             image = item.variant.images.first()
#             if image:
#                 item.image_url = image.image.url

#     return render(request, 'order_items.html', {
#         'order': order,
#         'order_items': order_items,
#     })


# views.py

# from django.shortcuts import render, get_object_or_404
# from .models import Order, OrderItem, ProductImage

# def order_items(request, order_id):
#     order = get_object_or_404(Order, order_id=order_id)
#     items = OrderItem.objects.filter(order=order).select_related('variant', 'product')

#     # Load the first image per variant
#     images = {}
#     for item in items:
#         image = ProductImage.objects.filter(variant=item.variant).first()
#         images[item.variant.id] = image

#     return render(request, 'order_items.html', {
#         'order': order,
#         'items': items,
#         'images': images
#     })


def order_items(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    items = OrderItem.objects.filter(order=order).select_related('product')

    # Attach image to each item
    for item in items:
        item.image = ProductImage.objects.filter(variant__product=item.product).first()

    return render(request, 'order_items.html', {
        'order': order,
        'items': items,
    })




from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, CancelOTP
import random
from django.core.mail import send_mail

# def initiate_cancel_order(request, order_id):
#     if request.method == 'POST':
#         order = get_object_or_404(Order, order_id=order_id)
#         request.session['cancel_order_id'] = order.order_id
#         return render(request, 'cancel_confirm_email.html')  # A form to get user's email



# def initiate_cancel_order(request, order_id):
#     if request.method == 'POST' and 'email' in request.POST:
#         email = request.POST['email']
#         otp = str(random.randint(100000, 999999))

#         CancelOTP.objects.create(email=email, otp=otp, order_id=order_id)

#         send_mail(
#             'Your OTP to Cancel Order',
#             f'Your OTP is: {otp}',
#             'your_email@example.com',
#             [email],
#         )
#         request.session['cancel_email'] = email
#         return redirect('verify_cancel_otp')
#     return render(request, 'cancel_confirm_email.html')


from django.contrib import messages
from django.core.mail import send_mail
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, CancelOTP, mainuser

def initiate_cancel_order(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST['email']
        try:
            user = mainuser.objects.get(user_id=user_id)
        except mainuser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('my_orders')

        if user.user_mail != email:
            messages.error(request, "The entered email does not match your account.")
            return render(request, 'cancel_confirm_email.html')

        otp = str(random.randint(100000, 999999))

        CancelOTP.objects.create(email=email, otp=otp, order_id=order_id)

        send_mail(
            'Your OTP to Cancel Order',
            f'Your OTP is: {otp}',
            'your_email@example.com',
            [email],
        )

        request.session['cancel_email'] = email
        request.session['cancel_order_id'] = order_id
        return redirect('verify_cancel_otp')

    return render(request, 'cancel_confirm_email.html')


def verify_cancel_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        order_id = request.session.get('cancel_order_id')
        email = request.session.get('cancel_email')

        otp_record = CancelOTP.objects.filter(order_id=order_id, email=email).order_by('-created_at').first()

        if otp_record and otp_record.otp == entered_otp:
            order = get_object_or_404(Order, order_id=order_id)
            order.status = 'Cancelled'
            order.save()
            CancelOTP.objects.filter(order=order).delete()  # Clean up
            return redirect('my_orders')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')



def track_order(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    order = get_object_or_404(Order, order_id=order_id, user_id=user_id)

    # Step order
    steps = [
        'Pending',
        'Processing',
        'Quality Check',
        'Shipped',
        'Delivered'
    ]

    current_step = steps.index(order.status) if order.status in steps else -1

    context = {
        'order': order,
        'steps': steps,
        'current_step': current_step,
    }
    return render(request, 'track_order.html', context)

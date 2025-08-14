from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Link
from .utils import generate_code
from django.db import IntegrityError
import validators

# Create your views here.

BASE_URL = "http://127.0.0.1:8000"  # Change when deploying

def home(request):
    short_url = None

    if request.method == "POST":
        original_url = request.POST.get("original_url", "").strip()
        custom_alias = request.POST.get("custom_alias", "").strip()

        # Validate URL input
        if not original_url:
            messages.error(request, "Please enter a URL.")
            return redirect("home")

        if not (original_url.startswith("http://") or original_url.startswith("https://")):
            original_url = "http://" + original_url

        if not validators.url(original_url):
            messages.error(request, "Invalid URL.")
            return redirect("home")

        # Handle alias validation
        if custom_alias:
            if len(custom_alias) < 3 or len(custom_alias) > 16:
                messages.warning(request, "Alias must be 3–16 characters.")
                return redirect("home")
            code = custom_alias
        else:
            code = generate_code()

        
        try:
            link = Link(original_url=original_url, short_code=code)
            link.save()
        except IntegrityError:
            if custom_alias:  
                messages.error(request, "Alias already exists. Please choose another one.")
                return redirect("home")
            else:
                
                while True:
                    code = generate_code()
                    if not Link.objects.filter(short_code=code).exists():
                        break
                link = Link(original_url=original_url, short_code=code)
                link.save()

        short_url = f"{BASE_URL}/{link.short_code}"
        return render(request, "index.html", {
            "short_url": short_url,
            "original_url": original_url
        })

    return render(request, "index.html")


def redirect_url(request, code):
    link = get_object_or_404(Link, short_code=code)
    link.clicks += 1
    link.save()
    return redirect(link.original_url)

def admin_links(request):
    links = Link.objects.order_by("-created_at")
    return render(request, "admin.html", {"links": links, "base": BASE_URL})

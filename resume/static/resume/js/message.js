const postForm = document.querySelector("#contact-form");


function handleSubmit(postForm) {
    postForm.addEventListener("submit", e => {
        e.preventDefault();
        formData = new FormData(postForm);
        fetch('/message', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                postForm.reset();
                document.querySelector("#notify").innerHTML = `<div class="alert alert-success alert-dismissible show" role="alert">
                                                                  <strong>Success!</strong> Thank you <strong>${data.name}</strong> for your message.
                                                                </div> `
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    })
}

handleSubmit(postForm)
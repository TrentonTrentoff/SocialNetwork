document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.edit').addEventListener('click', edit_post);
    // Waiting for post to be submitted
    document.querySelector('#compose-post').onsubmit = send_post;
  });

function edit_post(post) {
  console.log("DO EDIT STUFF");
  document.querySelector('.post-body').innerHTML = "GET FUCKED";
  return false
}

function send_post() {

}
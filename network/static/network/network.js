document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(edit => {
      edit.onclick = function() {
        edit_post(this.id);
        return false;
        }
      })
    // Waiting for post to be submitted
    // document.querySelector('#compose-post').onsubmit = send_post;
  });

function edit_post(editpost_id) {
  const post_id = editpost_id.substring(5);
  const originalPost = document.getElementById(`body_${post_id}`);
  const originalPostText = originalPost.textContent;
  let newPost = document.createElement('textarea');
  newPost.innerHTML = originalPostText;
  originalPost.append(newPost);
}

function send_post() {

}
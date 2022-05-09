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
  newPost.id = "currentlyEditing";
  let sendPost = document.createElement('input');
  sendPost.setAttribute("type", "submit");
  newPost.innerHTML = originalPostText;
  sendPost.addEventListener('click', function () {
    send_post(post_id);
  })
  originalPost.append(newPost);
  originalPost.append(sendPost);
}

function send_post(post_id) {
  fetch('/edit', {
    method: 'POST',
    body: {
      id: post_id,
      body: document.querySelector('#currentlyEditing').value
      }
    })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    load_mailbox('Edited!')
    })
  console.log("This ran");
  return false;
}
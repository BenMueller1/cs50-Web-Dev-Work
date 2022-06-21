document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#submit_email').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function send_email()  {
  // after we hit submit, the form will still be there so we can get the values of its fields, it will onle dissapear once we load another page
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => load_mailbox('sent'))
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // need to add to this, make a GET request to load the data for the appropriate mailbox, then add html elements (implement infinite scroll)
  // in order to show all of the emails
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';
  emailView = document.querySelector('#emails-view') 

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get all emails in mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach((email) => {
        //console.log(email)
        let d = document.createElement('div');
        d.id = `email-${email["id"]}`
        d.innerHTML = `<p>From: ${email["sender"]}, Subject: ${email["subject"]}, Timestamp: ${email["timestamp"]} <button id="button-${email['id']}">View</button> </p>`;
        if (email["read"]) {
          d.style.background = "grey";
        }
        else {
          d.style.background = "white";
        }
        emailView.append(d)
        document.querySelector(`#button-${email['id']}`).addEventListener('click', () => view_email(email, mailbox));
      })
  })
}


function view_email(email, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';
  viewEmail = document.querySelector('#view-email');
  viewEmail.innerHTML = "";

  // mark email as read
  fetch(`emails/${email['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  let e = document.createElement('div');
  e.innerHTML = `<p>From: ${email["sender"]}, To: ${email["recipients"]}, Subject: ${email["subject"]}, 
    Timestamp: ${email["timestamp"]}, Body: ${email["body"]}</p>`
  
  viewEmail.append(e)

  // if mailbox === "inbox", we want to give user the option to archive / unarchive email
  if (mailbox !== "sent") {
    if (email['archived']) {
      e.innerHTML += `<button id="unarchive-${email['id']}"> Unarchive </button>`;
      document.querySelector(`#unarchive-${email['id']}`).addEventListener('click', () => archive(email, false));
    }
    else {
      e.innerHTML += `<button id="archive-${email['id']}"> Archive </button>`;
      document.querySelector(`#archive-${email['id']}`).addEventListener('click', () => archive(email, true));
    }
  }
  
}


function archive(email, bool) {
  fetch(`/emails/${email['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: bool
    })   
  })
  load_mailbox('inbox');
}


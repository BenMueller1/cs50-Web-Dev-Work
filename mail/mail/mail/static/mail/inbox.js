document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox', true));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent', true));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive', true));
  document.querySelector('#compose').addEventListener('click', () => compose_email(true));

  document.querySelector('#submit_email').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox', true);
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
  .then(response => load_mailbox('sent', true))
}

// push_history is a boolean that tells us if we should push this state to the history or not
// if we have hit the back arrow to get to the current page, we don't want to push it to history (would create infinite loop)
function compose_email(push_history) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  if(push_history) {
    history.pushState({"page": "compose", "email":null}, "", "");
  }
  
}

function load_mailbox(mailbox, push_history) {
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
        document.querySelector(`#button-${email['id']}`).addEventListener('click', () => view_email(email, mailbox, true));
      })
  })
  if(push_history) {
    history.pushState({"page": mailbox, "email":null}, "", "");
  }
  

}


function view_email(email, mailbox, push_history) {
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

  // if mailbox === "inbox", we want to give user the option to archive / unarchive email and the option to reply
  if (mailbox !== "sent") {
    if (email['archived']) {
      e.innerHTML += `<button id="unarchive-${email['id']}"> Unarchive </button>`;
      document.querySelector(`#unarchive-${email['id']}`).addEventListener('click', () => archive(email, false));
    }
    else {
      e.innerHTML += `<button id="archive-${email['id']}"> Archive </button>`;
      document.querySelector(`#archive-${email['id']}`).addEventListener('click', () => archive(email, true));
    }

    // reply button
    e.innerHTML += `<button id="reply-${email['id']}"> Reply </button>`
    document.querySelector(`#reply-${email['id']}`).addEventListener('click', () => reply(email, true));
  }
  
  history.pushState({"page": "view_email", "email":email}, "", "");
}


function reply(email, push_history) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Autofill composition fields
  document.querySelector('#compose-recipients').value = `${email['sender']}`;
  document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
  document.querySelector('#compose-body').value = `On Jan 1 2020, 12:00 AM ${email['sender']} wrote: ${email['body']}`;
  // avoiding "Re: Re: " if we have a reply to a reply
  let sub = document.querySelector('#compose-subject').value
  if (sub.slice(0,8) === "Re: Re: ") {
    document.querySelector('#compose-subject').value = sub.slice(4);
  }

  if(push_history) {
    history.pushState({"page": "reply", "email":email}, "", "");
  }
  
}


function archive(email, bool) {
  fetch(`/emails/${email['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: bool
    })   
  })
  load_mailbox('inbox', true);
}


window.onpopstate = function(event) {
  // console.log('is it called?')
  // console.log(event.state)
  // console.log(event.state['page'])
  console.log(history)
  // event.state will hold the data we pass (page could be inbox, sent, archive, compose, view_email, or reply) (email could be an email or null)
  // this data should tell us what page we should load
  switch(event.state['page']) {  // do I need to use breacket notation?
    case "inbox":
      load_mailbox('inbox', false);
      break;
    case "sent":
      load_mailbox('sent', false);
      break;
    case "archive":
      load_mailbox('archive', false);
      break;
    case "compose":
      compose_email(false);
      break;
    case "view_email":
      view_email(event.state['email'], event.state['page'], false);
      break;
    case "reply":
      reply(event.state.email, false);
      break;
  }
}
<script lang="ts">
	export let contacts: any;
	import type { PageData } from './$types';
	import { session } from '$lib/store/user.store';
	import { messages, sendMessage } from '$lib/store/message.store';
	import { browser } from '$app/environment';
	import { page } from '$app/stores';
	import { BASE_URI_DOMAIN, BASE_API_URI } from '$lib/constants';
	import type { Message } from '$lib/types/message.interface';
	import { element } from 'svelte/internal';
	
	

	function trial2(event: MouseEvent, contact, id) {
		window.location.assign("/chat/" + contact['task_id'])
	}
	
	function trial(event: MouseEvent, contact, id) {
		let messageInput: string, socket: WebSocket;
		// let href = document.getElementById("contact" + id).href
		// if (href != "dummy.com"){
		// 	document.getElementById("contact").href = "/chat/" + contact.fields.username;
		// }
		if (browser) {
			const websocketUrl = `${
				$page.url.protocol.split(':')[0] === 'http' ? 'ws' : 'wss'
			}://${BASE_URI_DOMAIN}/ws/chat/${id}/?${$session.user.pk}`;

			socket = new WebSocket(websocketUrl);

			socket.addEventListener('open', () => {
				console.log('Connection established with!' + id);
			});

			socket.addEventListener('message', (event) => {
				const data = JSON.parse(event.data);
				const messageList: Array<Message> = JSON.parse(data.messages).map((message: any) => {
					return {
						message: message.fields.message,
						thread_name: message.fields.thread_name,
						timestamp: message.fields.timestamp,
						sender__pk: message.fields.sender__pk,
						sender__username: message.fields.sender__username,
						sender__last_name: message.fields.sender__last_name,
						sender__first_name: message.fields.sender__first_name,
						sender__email: message.fields.sender__email,
						sender__is_staff: message.fields.sender__is_staff,
						sender__is_active: message.fields.sender__is_active,
						sender__is_superuser: message.fields.sender__is_superuser,
						file: message.fields.file,
						filename: message.fields.filename
					};
				});
				$messages = messageList;
				messageInput = '';
			});
			// document.getElementById("contact").href = "/chat/" + contact.fields.username;

			console.log(
				BASE_API_URI + '/chat/' + contact.fields.username + '/?username=' + $session.user.pk
			);
			console.log(contact.accepted);
			window.location.href =
				'/chat/' +
				contact.fields.username +
				'/?username=' +
				$session.user.username +
				'&id=' +
				$session.user.pk;
		}
	}

	function myfun(task_id, status){
		// console.log("l" + task_id)
		// var ele = document.getElementById("task_" + task_id)
		// ele.style.backgroundColor = "#E3E3E3";
		$session.current_task = task_id
		$session.current_task_status = status
		// console.log(`${$session.current_task}`)
		return null
	}

	function trial3(x){
		if (x === "completed"){
			return "Inactive";
		}
		else if (x === "pending"){
			return "Waiting";
		}
		else{
			return "Active";
		}
	}
	
</script>

<div class="card">
	<div class="card-body">
		<ul class="list-unstyled mb-0">
			{#each contacts as contact, id}
				<li class="p-2" class:border-bottom={id + 1 !== contacts.length} id="task_{contact["task_id"]}">
					<!-- <a id="contact{id}" href={null} on:click={(event) => trial(event, contact, id)} class="d-flex justify-content-between"> -->
					<!-- <div
						on:click={(event) => trial2(event, contact, id)}
						class="d-flex justify-content-between"
					> -->
					<a href="/chat/{contact['task_id']}/" on:click={myfun(contact['task_id'], contact['task_status'])} class="d-flex justify-content-between" >
						<div class="d-flex flex-row" >
							<img
								src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-{id + 1}.webp"
								alt="avatar"
								class="rounded-circle d-flex align-self-center me-3 shadow-1-strong"
								width="60"
							/>
							
							<div class="pt-1">
								<p class="fw-bold mb-0">
									Task ID: {contact['task_id']}
								</p>
							</div>
							<div class="pt-1" style="position: absolute; right:10px;">
								<p class="fw-bold mb-0 flex-row" style="color: black;">
									({trial3(contact['task_status'])})
								</p>
							</div>
						</div>
					</a>
				</li>
			{/each}
		</ul>
	</div>
</div>

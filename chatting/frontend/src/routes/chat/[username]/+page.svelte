<script lang="ts">
	import type { PageData } from './$types';
	import Contact from '$lib/components/Contacts/Contact.svelte';
	import { session } from '$lib/store/user.store';
	import You from '$lib/components/Message/You.svelte';
	import YouFile from '$lib/components/Message/YouFile.svelte';
	import Other from '$lib/components/Message/Other.svelte';
	import OtherFile from '$lib/components/Message/OtherFile.svelte';
	import { messages, sendMessage } from '$lib/store/message.store';
	import { browser } from '$app/environment';
	import { page } from '$app/stores';
	import { BASE_URI_DOMAIN } from '$lib/constants';
	import type { Message } from '$lib/types/message.interface';
	export let data: PageData;
	console.log(data.context);
	var fullName = `${$session.current_task}`;

	import { BASE_API_URI } from '$lib/constants';
	let messageInput: string, socket: WebSocket, fileinput: File, filename: string;
	if (browser) {
		// var u1 = parseInt(${JSON.parse(data.context.user_object.toString())[0].pk});
		// if (JSON.parse(data.context.user_object)[0].pk < session.user.pk ) {
		// 	greeting = "Good day";
		// }
		// else {
		// 	greeting = "Good evening";
		// }
		fullName = `${$session.current_task}`;
		const websocketUrl = `${
			$page.url.protocol.split(':')[0] === 'http' ? 'ws' : 'wss'
		}://${BASE_URI_DOMAIN}/ws/chat/${data.context['task_object']['task_id']}/?${$session.user.pk}`;

		socket = new WebSocket(websocketUrl);

		socket.addEventListener('open', () => {
			console.log('Connection established!');
		});

		socket.addEventListener('message', (event) => {
			const data = JSON.parse(event.data);
			const messageList: Array<Message> = JSON.parse(data.messages).map((message: any) => {
				return {
					msg_id: message.pk,
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
	}
	console.log('Hi');
	function getConn() {
		const websocketUrl = `${
			$page.url.protocol.split(':')[0] === 'http' ? 'ws' : 'wss'
		}://${BASE_URI_DOMAIN}/ws/chat/${data.context['task_object']['task_id']}/?${$session.user.pk}`;

		socket = new WebSocket(websocketUrl);

		socket.addEventListener('open', () => {
			console.log('Connection established!');
		});

		socket.addEventListener('message', (event) => {
			const data = JSON.parse(event.data);
			const messageList: Array<Message> = JSON.parse(data.messages).map((message: any) => {
				return {
					msg_id: message.pk,
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
	}
	function myfunc() {
		return new Promise((resolve) => {
			resolve(getConn());
		});
	}

	function sleep(time: number) {
		return new Promise((resolve) => setTimeout(resolve, time));
	}

	// Usage!

	async function handleSendMessage(event: MouseEvent) {
		event.preventDefault();
		// let t = await myfunc();
		getConn();

		sleep(1000).then(() => {
			let task_obj = data.context['task_object'];
			if (task_obj.task_status === 'completed') {
				alert('Task is completed! Chat disabled.');
			} else {
				sendMessage(messageInput, fileinput, $session.user.username as string, filename, socket);
			}
		});

		// myfunc().then(() => {
		// // Do something after the sleep!
		// 	console.log("hihihi");
		// 	sendMessage(messageInput, $session.user.username as string, socket);
		// });
		// if (browser) {
		// 	// var u1 = parseInt(${JSON.parse(data.context.user_object.toString())[0].pk});
		// 	// if (JSON.parse(data.context.user_object)[0].pk < session.user.pk ) {
		// 	// 	greeting = "Good day";
		// 	// }
		// 	// else {
		// 	// 	greeting = "Good evening";
		// 	// }
		// 	const websocketUrl = `ws://${BASE_URI_DOMAIN}/ws/chat/${
		// 		JSON.parse(data.context.user_object)[0].pk
		// 	}/?${$session.user.pk}`;

		// 	socket = new WebSocket(websocketUrl);

		// }
		// if (browser) {
		// var u1 = parseInt(${JSON.parse(data.context.user_object.toString())[0].pk});
		// if (JSON.parse(data.context.user_object)[0].pk < session.user.pk ) {
		// 	greeting = "Good day";
		// }
		// else {
		// 	greeting = "Good evening";
		// }

		// myfunc().then(
		// 	function(value){
		// 	sendMessage(messageInput, $session.user.username as string, socket);
		// 	}
		// );
	}
	var file;
	const uploadFile = (): Promise<string> => {
		return new Promise((resolve) => {
			resolve(document.getElementById('input-file').click());
		});
	};
	const clickSubmit = (): Promise<string> => {
		return new Promise((resolve) => {
			resolve(document.getElementById('submit-file').click());
		});
	};

	const getFile = (): Promise<string> => {
		return new Promise((resolve) => {
			resolve(document.getElementById('input-file').click());
		});
	};

	// async function handleSendFile (event: MouseEvent) {
	// 	// event.preventDefault();

	// 	// sendMessage(messageInput, $session.user.username as string, socket);
	// 	// var temp = await document.getElementById('input-file').click();
	// 	// file =  document.getElementById('input-file').files;
	// 	var x = await document.getElementById('submit-file')?.click();

	// };

	const handleSendFile = async (event: MouseEvent) => {
		console.log('submit');
		var t = await uploadFile();
		var t2 = (await clickSubmit()) && t;
		file = document.getElementById('input-file').files;
		console.log(file);
	};

	let fileData: string;

	const readFile = (file: File): Promise<string> => {
		return new Promise((resolve) => {
			const reader = new FileReader();
			console.log(reader.result);
			reader.onload = () => resolve(reader.result as string);
			if (file) {
				reader.readAsDataURL(file);
				console.log(reader.result);
			}
		});
	};

	const handleFileUpload = async (event: SubmitEvent) => {
		// console.log("ji")
		const formData = new FormData(event.target as HTMLFormElement);
		const file = formData.get('file') as File;
		console.log('Here', file);
		// fileData = await readFile(file);
		// console.log("Here again");
		// console.log(fileData)
		sendMessage(messageInput, file, $session.user.username as string, file.name, socket);
		// send(fileData);
	};

	function send(file: string) {
		getConn();
		sleep(100).then(() => {
			sendFile(file, $session.user.username as string, socket);
		});
		sleep(100).then(() => {
			console.log('File sent');
		});
	}

	// const handleFileUpload = async (event: SubmitEvent) => {
	// 	file =  await document.getElementById('input-file').files[0];

	// };
	console.log($session.current_task_status)
	if ($session.current_task_status === "completed"){
		document.getElementById("message-body").disabled = true;
		// msg_inp.disabled = true;
	}

</script>

<div class="container ">
	<div class="row" style="padding-top:8%; margin-top: 0%;">
		<div class="tp col-md-6 col-lg-5 col-xl-4 mb-4 mb-md-0 scrollable">
			<h5 class="font-weight-bold mb-3 text-center text-lg-start">
				{$session.user.username}'s Tasks
			</h5>
			<Contact contacts={data.context['tasks']['accepted']} />
		</div>
		<div class="col-md-6 col-lg-7 col-xl-8" id="message-wrapper">
			<div>
				<h5 class="font-weight-bold mb-3 text-center text-lg-start">
					{`${$session.current_task}`}
				</h5>
			</div>
			<div class="scrollable" style="background-color: #E3E3E3; padding:3%; height: 5px;">
				<ul class="list-unstyled" id="chat-body">
					{#each $messages as message, id}
						{#if message.sender__pk === $session.user.pk}
							{#if message.filename}
								<YouFile {message} />
							{:else}
								<You {message} />
							{/if}
						{:else if message.filename}
							<OtherFile {message} />
						{:else}
							<Other {message} />
						{/if}
					{/each}
				</ul>
			</div>
			<iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
			<form method="post" action="http://localhost:9030/api/uploadFile/?taskId={data.context['task_object']['task_id']}&senderUsername={$session.user.username}&output=embed" enctype="multipart/form-data" target="dummyframe">
				<div class="group">
					<input type="file" id="file-upload" name="file" />
				</div>

				<button type="submit">Submit</button>
			</form>

			<div
				class="text-muted d-flex justify-content-start align-items-center pe-3 pt-3 mt-2 message-control"
			>
				<img
					src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-{$session.user.pk}.webp"
					alt="You"
					title="You"
					style="width: 40px; height: 100%"
				/>
				<textarea
					placeholder="Type message"
					class="form-control form-control-lg"
					id="message-body"
					rows="1"
					disabled={$session.current_task_status === "completed"}
					bind:value={messageInput}
				/>

				<a
					class="ms-3"
					id="send-message-btn"
					title="Send"
					href={null}
					on:click={(event) => handleSendMessage(event)}
				>
					<i class="fas fa-paper-plane" />
				</a>
				<!-- <a
					class="ms-3"
					id="send-file-btn"
					title="Send"
					href={null}
					on:click={(event) => handleSendFile(event)}
				>
					<i class="fas fa-paperclip" />
				</a> -->
			</div>
		</div>
	</div>
</div>

<style>
	@media screen and (max-width: 768px) {
		.tp {
			margin-top: 200%;
		}
	}
</style>

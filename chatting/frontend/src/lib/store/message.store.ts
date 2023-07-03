import type { Message } from '$lib/types/message.interface';
import { writable, type Writable } from 'svelte/store';

const newMessages = () => {
	const { subscribe, update, set }: Writable<Array<Message>> = writable([]);

	return { subscribe, update, set };
};

const messages = newMessages();

// const socket = new WebSocket('wss://dae9057c.ngrok.io');

// // Connection opened
// socket.addEventListener('open', function (_event) {
// 	console.log('Connection established!');
// });

// // Listen for messages
// socket.addEventListener('message', function (event) {
// 	messages.set(event.data);
// });

const sendMessage = (message: string, file: File, senderUsername: string, filename: string, socket: WebSocket) => {
	if (socket.readyState <= 1) {
		console.log(file)
		const reader = new FileReader();

		var success = function (content) {
			console.log(JSON.stringify(content));
		}
		reader.onload = function (evt) { success(evt.target.result) };

		// console.log(reader.readAsDataURL(file))
		// reader.onload = (e) => {
		// 	if(e){
		// 		base64_data = e.data;
		//     	base64_value(base64_data)
		// 	}

		// }
		if ((!!file) || message != "") {
			socket.send(
				JSON.stringify({
					message: message,
					senderUsername: senderUsername,
					file: file,
					filename: filename,
				})
			);
		}
	}
};

const sendmess = (file: File, senderUsername: string, filename: string, socket: WebSocket) => {
	if (socket.readyState <= 1) {
		socket.send(
			JSON.stringify({
				file: file,
				filename: filename,
				senderUsername: senderUsername
			})
		);
	}
};

export { messages, sendMessage };

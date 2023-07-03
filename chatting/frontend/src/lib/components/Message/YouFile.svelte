<script lang="ts">
	import { BASE_API_URI, timeSince } from '$lib/constants';
	import type { Message } from '$lib/types/message.interface';

	function handleDownloadFile(event: MouseEvent) {
		event.preventDefault();
		// let t = await myfunc();
		// http://10.129.2.174:9030/api/downloadFile/?taskId=82
		// console.log(BASE_API_URI + "/downloadFile/?taskId=" + message.thread_name + "&timestamp=" + message.timestamp + "&senderUsername=" + message.sender__username)
		// const chat_res = await fetch(
		// 	`${BASE_API_URI}/downloadFile/?taskId=${message.thread_name}&timestamp=${message.timestamp}&senderUsername=${message.sender__username}`
		// );
		var xhttp = new XMLHttpRequest();
		var url = BASE_API_URI + "/downloadFile/?taskId=" + message.thread_name+ "&msg_id=" + message.msg_id + "&timestamp=" + message.timestamp + "&senderUsername=" + message.sender__username;
		xhttp.onreadystatechange = function() {
		var a, today;
		if (xhttp.readyState === 4 && xhttp.status === 200) {
			a = document.createElement('a');
			a.href = window.URL.createObjectURL(xhttp.response);
			console.log(xhttp.response)
			today = new Date();
			a.download = message.filename;
			a.style.display = 'none';
			document.body.appendChild(a);
			return a.click();
		}
		};
		xhttp.open("GET", url, true);
		xhttp.setRequestHeader("Content-Type", "application/json");
		xhttp.responseType = 'blob';
		xhttp.send();
		}

	export let message: any;
</script>

<li class="d-flex justify-content-end mb-4">
	<div class="card">
		<div class="card-header d-flex justify-content-between p-3">
			<p class="fw-bold mb-0">
				{message.sender__first_name + ' ' + message.sender__last_name}(You)
			</p>
			<p class="text-muted small mb-0">
				<i class="far fa-clock" />
				{timeSince(message.timestamp)}
			</p>
		</div>
		<div class="card-header d-flex justify-content-between p-3">
			<div class="card-body">
				<p class="mb-0">{message.filename}</p>
			</div>
			<div class="card-body">
				<a	class="ms-3"
					id="download-btn"
					title="Download"
					href={null}
					on:click={(event) => handleDownloadFile(event)}
					>
						
					<i class="fa fa-download" />
				</a>
			</div>
		</div>
		
	</div>
	<img
		src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-{message.sender__pk}.webp"
		alt="You"
		title="You"
		class="rounded-circle d-flex align-self-start me-3 shadow-1-strong"
		width="60"
	/>
</li>

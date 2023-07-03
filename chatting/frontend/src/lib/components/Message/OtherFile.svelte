<script lang="ts">
	import { BASE_API_URI, timeSince } from '$lib/constants';

	export let message: any;

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
	

</script>

<li class="d-flex justify-content-start mb-4">
	<img
		src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-{message.sender__pk}.webp"
		alt={message.sender__username}
		title={message.sender__username}
		class="rounded-circle d-flex align-self-start ms-3 shadow-1-strong"
		width="60"
	/>
	<div class="card">
		<div class="card-header d-flex justify-content-between p-3">
			<p class="fw-bold mb-0">
				{message.sender__first_name + ' ' + message.sender__last_name}
			</p>
			<p class="text-muted small mb-0">
				<i class="far fa-clock" />
				{timeSince(message.timestamp)}
			</p>
		</div>
		<div class="card-body">
			<p class="mb-0">{message.filename}</p>
		</div>
		<div class="card-body">
			<a	class="ms-3"
				id="download-btn"
				title="download"
				href={null}
				on:click={(event) => handleDownloadFile(event)}
				>
					
				<i class="fa fa-download" />
			</a>
		</div>
	</div>
</li>

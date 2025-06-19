const url = "http://localhost:8000/api/candidate";

async function handleDeleteUser(user_id) {
	try {
		const response = await fetch(`${url}/delete/${user_id}`);
		if(!response.ok) {
			console.log("something went wrong: Deleting user failed");
			return;
		}

		window.location.href = "http://localhost:8000";
	} catch(err) {
		console.log(err)
	}
}

function handleModal(close = false) {
	const modalShow = document.getElementById("show");
	if(modalShow) {
		modalShow.style.display = close ? "none" : "block";
	}
}

function updateModal(candidateData) {
	const sanitisedJSON = candidateData.replace(/'/g, '"');
	const candidate = JSON.parse(sanitisedJSON);
  handleModal(false);
	document.querySelector("#candidate-id").value = candidate.id;
  document.querySelector("input[name='name']").value = candidate.name;
  document.querySelector("input[name='email']").value = candidate.email;
  document.querySelector("input[name='phone_number']").value = candidate.phone_number;
  document.querySelector("input[name='age']").value = candidate.age;
	document.querySelector(`input[name="status"][value="${candidate.status}"]`).checked = true;

  const isFemale = candidate.gender === "F";
  document.querySelector("input[type='checkbox']").checked = isFemale;
}

async function submitModalForm (e) {
  e.preventDefault();
	const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
	const genderCheckbox = form.querySelector('input[type="checkbox"]');
  data.gender = genderCheckbox.checked ? "F" : "M";
	const isUpdate = !!data.id;

	const formUrl = isUpdate
	? `${url}/update/${data.id}`
	: `${url}/create`;

	const { id, csrfmiddlewaretoken, ...candidateData } = data

  const res = await fetch(formUrl, {
    method: isUpdate ? "PATCH": "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: JSON.stringify([candidateData]),
  });

  const result = await res.json();

  if (res.ok) {
    form.reset();
		handleModal(true);
  } else {
    console.error(result);
    alert("Validation failed");
  }
};

function debounce(func, delay) {
	let timer;
	return function (...args) {
		clearTimeout(timer);
		timer = setTimeout(() => func.apply(this, args), delay);
	};
}

const searchInput = document.getElementById("search");
const resultBox = document.getElementById("trackersearchresults");
const resultBoxItems = document.getElementById("trackersearchresultitems");

async function fetchSearchResults(query) {
	if (query.trim().length === 0) {
		resultBox.style.display = "none";
		resultBox.innerHTML = "";
		return;
	}

	try {
		const response = await fetch(`${url}/search/${encodeURIComponent(query)}`);
		
		if(!response.ok) {
			console.log("User search failed... ");
			return;
		}

		const data = await response.json();
		const foundCandidates = data?.data;

		if (foundCandidates.length > 0) {
			resultBoxItems.innerHTML = foundCandidates.map(candidate => `
				<a class="trackersearchresultitem waves-effect waves-light" href="/candidate/${candidate.id}">
					<img src="/static/img/patcher.png" class="tracksearchpic" alt="user_pic" />
					<div class="trackersearchname">${candidate.name}</div>
				</a>
			`).join("");
		} else {
			resultBox.innerHTML = `
				<div class="trackersearchresultitem">
					<div class="trackersearchname">
						No results
					</div>
				</div>
			`;
		}
		resultBox.style.display = "block";
	} catch(err) {
		console.log("Something went wrong: searching user failed...")
	}
}

const debouncedFetch = debounce((e) => fetchSearchResults(e.target.value), 300);
searchInput.addEventListener("input", debouncedFetch);

function addPost(postData) {
    const display=document.getElementById("display");
    const imageUrl = postData.image_url ? postData.image_url : "../assets/post.png";

    const timestamp = new Date(postData.timestamp);
    const date = timestamp.toLocaleDateString();
    const time = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const sessionUserId = sessionStorage.getItem("userId");

    const postCard = document.createElement("div");
    postCard.id = postData.post_id;
    postCard.setAttribute("data-user-id", postData.user_id);
    postCard.className = "w-72 h-fit rounded-xl shadow-lg overflow-hidden flex flex-col border-2 border-black cursor-pointer";

    postCard.onclick = () => {
        localStorage.setItem("selectedPost", JSON.stringify(postData));
        window.location.href = "post.html";
    };

    postCard.innerHTML = `
        <div class="relative w-full h-48 overflow-hidden border-b border-slate-950">
            <img src="${imageUrl}" alt="Post Image" class="w-full h-full object-cover" />
        </div>
        <div class="flex flex-col justify-between p-4 flex-grow bg-slate-950">
            <div>
                <h4 class="text-base font-semibold text-blue-400 hover:text-blue-500 transition leading-snug line-clamp-2">
                    ${postData.title}
                </h4>
                <p class="text-xs text-gray-400 mt-2 line-clamp-4 leading-relaxed">
                    ${postData.content}
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1 text-gray-400 shrink-0">Category:</span>
                    <span class="text-white font-medium whitespace-nowrap overflow-hidden text-ellipsis inline-block max-w-[160px]">
                        ${postData.category_name}
                    </span>
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1 text-gray-400 shrink-0">Tags:</span>
                    <span class="text-white font-medium whitespace-nowrap overflow-hidden text-ellipsis inline-block max-w-[160px]">
                        ${postData.tags}
                    </span>
                </p>
                <p class="text-xs text-gray-400 mt-2">Posted by 
                    <span class="text-white font-medium">${postData.username}</span> 
                    on <span class="text-white">${date}</span> at <span class="text-white">${time}</span>
                </p>
            </div>
            <div class="mt-4 flex justify-between text-gray-300 border-t border-gray-600 pt-3">
    <span class="flex items-center gap-1 text-sm hover:text-yellow-300 cursor-pointer">
        <i class="fa-solid fa-bookmark text-yellow-300 text-xs"></i><span>${formatCount(postData.bookmark_count)}</span>
    </span>
    <span class="flex items-center gap-1 text-sm cursor-pointer">
        <i class="fa-solid fa-share-alt text-lime-300 text-xs"></i><span>${formatCount(postData.shared)}</span>
    </span>
    <span class="flex items-center gap-1 text-sm cursor-pointer">
        <i class="fa-solid fa-square-plus text-purple-500 text-xs"></i><span>${formatCount(postData.followed)}</span>
    </span>
    <span class="flex items-center gap-1 text-sm cursor-pointer">
        <i class="fa-solid fa-flag text-red-600 text-xs"></i>
    </span>
</div>
<div class="flex justify-between text-sm text-gray-300 mt-4 border-t border-gray-600 pt-3">
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-thumbs-up text-green-400"></i><span>${formatCount(postData.upvotes)}</span>
    </div>
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-thumbs-down text-red-400"></i><span>${formatCount(postData.downvotes)}</span>
    </div>
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-eye text-emerald-400"></i><span>${formatCount(postData.views)}</span>
    </div>
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-comment text-blue-400"></i><span>${formatCount(postData.comment_count)}</span>
    </div>
</div>
            </div>
        </div>
    `;

    display.appendChild(postCard);
}

async function fetchPopularPosts() {
    try {
        const response = await fetch('http://localhost:8000/post/Home');
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error fetching popular posts:', errorData);
            return;
        }

        const result = await response.json();
        const posts = result.data;
        if (Array.isArray(posts)) {
            posts.forEach(post => {
                addPost(post);
            });
        }

    } catch (error) {
        console.error('Error fetching popular posts:', error);
    }
}

fetchPopularPosts();

function formatCount(num) {
    if (num >= 1_000_000) {
        return (num / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
    } else if (num >= 1_000) {
        return (num / 1_000).toFixed(1).replace(/\.0$/, '') + 'k';
    } else {
        return num.toString();
    }
}

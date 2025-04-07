document.getElementById("addPost").addEventListener("click", () => {
    const modal = document.getElementById("postModal");
    modal.classList.remove("hidden");
    modal.classList.add("flex");
});

document.getElementById("close-post").addEventListener("click", () => {
    const modal = document.getElementById("postModal");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
});

document.getElementById("postImage").addEventListener("change", function () {
    const preview = document.getElementById("imagePreview");
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
    } else {
        preview.classList.add("hidden");
        preview.src = "";
    }
});

function createCategorySection(categoryName, categoryId) {
    const container = document.getElementById("category-container");

    const section = document.createElement("div");
    section.innerHTML = `
        <h2 class="text-xl font-semibold text-white mb-3">${categoryName}</h2>
        <div id="${categoryId}" class="flex gap-6 overflow-x-auto pb-2 hide-scrollbar">
            <!-- Posts will be added here -->
        </div>
    `;

    container.appendChild(section);
}

function addPostToCategory(categoryId, postData) {
    const category = document.getElementById(categoryId);

    const card = document.createElement("div");
    card.className = "min-w-[18rem] w-72 h-fit bg-gray-700 rounded-xl shadow-lg overflow-hidden flex flex-col border-2 shrink-0";
    card.innerHTML = `
        <div class="w-full h-48 overflow-hidden">
            <img src="${postData.image}" alt="Post Image" class="w-full h-full object-cover" />
        </div>
        <div class="flex flex-col justify-between p-4 flex-grow">
            <div>
                <h4 class="text-base font-semibold text-blue-400 hover:text-blue-500 transition leading-snug line-clamp-2">${postData.title}</h4>
                <p class="text-xs text-gray-400 mt-2 line-clamp-4 leading-relaxed">${postData.description}</p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1">Category:</span>
                    <span class="text-white font-medium">${postData.category}</span>
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1">Tags:</span>
                    <span class="text-white font-medium">${postData.tags}</span>
                </p>
                <p class="text-xs text-gray-400 mt-2">Posted by <span class="text-white font-medium">${postData.author}</span> on ${postData.date}</p>
            </div>
            <div class="mt-4 flex justify-between text-gray-300 border-t border-gray-600 pt-3">
                <button class="flex items-center gap-1 text-sm hover:text-yellow-300"><i class="fa-regular fa-bookmark text-yellow-300 text-xs"></i><span>${postData.bookmarks}</span></button>
                <button class="flex items-center gap-1 text-sm"><i class="fa-solid fa-share-alt text-lime-300 text-xs"></i><span>${postData.shares}</span></button>
                <button class="flex items-center gap-1 text-sm"><i class="fa-regular fa-square-plus text-purple-500 text-xs"></i><span>${postData.saves}</span></button>
                <button class="flex items-center gap-1 text-sm"><i class="fa-regular fa-flag text-red-300 text-xs"></i></button>
            </div>
            <div class="flex justify-between text-sm text-gray-300 mt-4 border-t border-gray-600 pt-3">
                <div class="flex items-center gap-1 text-xs"><i class="fa-solid fa-up-long text-green-400"></i><span>${postData.upvotes}</span></div>
                <div class="flex items-center gap-1 text-xs"><i class="fa-solid fa-down-long text-red-400"></i><span>${postData.downvotes}</span></div>
                <div class="flex items-center gap-1 text-xs"><i class="fa-regular fa-eye text-emerald-400"></i><span>${postData.views}</span></div>
                <div class="flex items-center gap-1 text-xs"><i class="fa-regular fa-comment text-blue-400"></i><span>${postData.comments}</span></div>
            </div>
        </div>
    `;

    category.appendChild(card);
}

const categoryData = [
    {
        name: "Trending",
        id: "trending-posts",
        posts: [
            {
                title: "10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything",
                description: "A deep dive into AI tools revolutionizing productivity, coding, and creativity.10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything10 AI Tools That Are Changing Everything",
                category: "Artificial Intelligence",
                tags: "AI, Tools, Future",
                author: "techSavvy",
                date: "April 6, 2025",
                image: "../assets/profile.png",
                bookmarks: 23,
                shares: 11,
                saves: 15,
                upvotes: 200,
                downvotes: 5,
                views: 1200,
                comments: 30
            },
            {
                title: "Why Web 3.0 is Gaining Traction Fast",
                description: "Everything you need to know about decentralized web and its impact.",
                category: "Web3",
                tags: "Blockchain, Future, Web3",
                author: "blockBoss",
                date: "April 4, 2025",
                image: "../assets/profile.png",
                bookmarks: 14,
                shares: 9,
                saves: 12,
                upvotes: 180,
                downvotes: 6,
                views: 1100,
                comments: 18
            },
            {
                title: "India's Tech Boom: Startups Rising",
                description: "How India is emerging as a global tech hub in 2025.",
                category: "Startups",
                tags: "India, Startups, Innovation",
                author: "desiCoder",
                date: "April 2, 2025",
                image: "../assets/profile.png",
                bookmarks: 20,
                shares: 7,
                saves: 10,
                upvotes: 175,
                downvotes: 4,
                views: 980,
                comments: 22
            },
            {
                title: "Top 5 Coding Challenges to Try This Month",
                description: "Boost your problem-solving skills with these challenges.",
                category: "Coding",
                tags: "DSA, Coding, Practice",
                author: "logicLord",
                date: "April 1, 2025",
                image: "../assets/profile.png",
                bookmarks: 12,
                shares: 4,
                saves: 7,
                upvotes: 150,
                downvotes: 2,
                views: 920,
                comments: 10
            },
            {
                title: "How ChatGPT is Reshaping Content Creation",
                description: "A look at how language models are powering bloggers and marketers.",
                category: "AI Tools",
                tags: "ChatGPT, Blogging, AI",
                author: "wordSmith",
                date: "March 30, 2025",
                image: "../assets/profile.png",
                bookmarks: 18,
                shares: 6,
                saves: 10,
                upvotes: 160,
                downvotes: 3,
                views: 1020,
                comments: 14
            }
        ]
    },
    {
        name: "Most Viewed",
        id: "most-viewed-posts",
        posts: [
            {
                title: "Mastering Tailwind CSS in 2025",
                description: "Learn how to build responsive designs quickly using utility-first CSS.",
                category: "Frontend",
                tags: "Tailwind, CSS, Web Design",
                author: "styleGuru",
                date: "April 3, 2025",
                image: "../assets/profile.png",
                bookmarks: 10,
                shares: 2,
                saves: 5,
                upvotes: 120,
                downvotes: 1,
                views: 2500,
                comments: 15
            },
            {
                title: "5 VS Code Extensions You Can't Miss",
                description: "Enhance your dev workflow with these powerful VS Code tools.",
                category: "Developer Tools",
                tags: "VS Code, Extensions, Productivity",
                author: "codeWhiz",
                date: "April 2, 2025",
                image: "../assets/profile.png",
                bookmarks: 8,
                shares: 5,
                saves: 6,
                upvotes: 140,
                downvotes: 0,
                views: 2400,
                comments: 11
            },
            {
                title: "React vs. Vue: Which One to Pick?",
                description: "A comprehensive comparison between two frontend giants.",
                category: "Frameworks",
                tags: "React, Vue, Comparison",
                author: "devBattle",
                date: "March 29, 2025",
                image: "../assets/profile.png",
                bookmarks: 15,
                shares: 4,
                saves: 9,
                upvotes: 130,
                downvotes: 2,
                views: 2100,
                comments: 20
            },
            {
                title: "Top 10 Google Fonts for Clean Design",
                description: "Make your UI pop with these professional Google Fonts.",
                category: "Design",
                tags: "Fonts, UI/UX, Web Design",
                author: "fontNinja",
                date: "March 27, 2025",
                image: "../assets/profile.png",
                bookmarks: 9,
                shares: 3,
                saves: 6,
                upvotes: 110,
                downvotes: 1,
                views: 2000,
                comments: 7
            },
            {
                title: "Gaming PCs Under ₹70,000 in India",
                description: "Best bang for buck builds in 2025.",
                category: "Gaming",
                tags: "PC Build, Gaming, Budget",
                author: "buildIt",
                date: "March 25, 2025",
                image: "../assets/profile.png",
                bookmarks: 17,
                shares: 5,
                saves: 11,
                upvotes: 160,
                downvotes: 2,
                views: 2700,
                comments: 25
            }
        ]
    },
    {
        name: "Recent Posts",
        id: "recent-posts",
        posts: [
            {
                title: "Google I/O 2025 Recap: What’s New",
                description: "Highlights from the latest event including Gemini and Android 15 updates.",
                category: "Tech News",
                tags: "Google IO, Android, AI",
                author: "eventBuzz",
                date: "April 6, 2025",
                image: "../assets/profile.png",
                bookmarks: 14,
                shares: 6,
                saves: 8,
                upvotes: 140,
                downvotes: 2,
                views: 1350,
                comments: 12
            },
            {
                title: "What’s New in Java 22?",
                description: "New features and improvements in the latest Java release.",
                category: "Programming",
                tags: "Java, Updates, JDK",
                author: "codeManiac",
                date: "April 5, 2025",
                image: "../assets/profile.png",
                bookmarks: 11,
                shares: 3,
                saves: 6,
                upvotes: 120,
                downvotes: 1,
                views: 900,
                comments: 8
            },
            {
                title: "How to Stay Focused While Coding",
                description: "Tips and habits to maintain deep focus during development.",
                category: "Productivity",
                tags: "Focus, Deep Work, Coding",
                author: "mindCoder",
                date: "April 4, 2025",
                image: "../assets/profile.png",
                bookmarks: 9,
                shares: 4,
                saves: 7,
                upvotes: 100,
                downvotes: 0,
                views: 850,
                comments: 6
            },
            {
                title: "Intro to Docker: Simplified",
                description: "Understand containers and get started with Docker the easy way.",
                category: "DevOps",
                tags: "Docker, Containers, Beginners",
                author: "devOpsly",
                date: "April 3, 2025",
                image: "../assets/profile.png",
                bookmarks: 13,
                shares: 5,
                saves: 9,
                upvotes: 115,
                downvotes: 1,
                views: 1000,
                comments: 10
            },
            {
                title: "Dark Mode Design Tips",
                description: "Designing with accessibility and aesthetic in mind for dark themes.",
                category: "UI/UX",
                tags: "Dark Mode, Accessibility, Design",
                author: "uiWizard",
                date: "April 2, 2025",
                image: "../assets/profile.png",
                bookmarks: 10,
                shares: 2,
                saves: 5,
                upvotes: 90,
                downvotes: 0,
                views: 780,
                comments: 4
            }
        ]
    },
    {
        name: "Popular Discussions",
        id: "popular-discussions",
        posts: [
            {
                title: "Do You Need a CS Degree in 2025?",
                description: "Community insights on whether formal education is necessary today.",
                category: "Career",
                tags: "CS Degree, Self-Taught, Jobs",
                author: "careerTalk",
                date: "April 6, 2025",
                image: "../assets/profile.png",
                bookmarks: 30,
                shares: 12,
                saves: 20,
                upvotes: 210,
                downvotes: 5,
                views: 1800,
                comments: 35
            },
            {
                title: "Is Rust Going to Replace C++?",
                description: "A heated community debate on whether Rust is the new standard.",
                category: "Programming Languages",
                tags: "Rust, C++, Comparison",
                author: "langFight",
                date: "April 5, 2025",
                image: "../assets/profile.png",
                bookmarks: 18,
                shares: 7,
                saves: 14,
                upvotes: 160,
                downvotes: 4,
                views: 1400,
                comments: 28
            },
            {
                title: "Remote Work in 2025: Still a Thing?",
                description: "Developers weigh in on how remote culture is evolving post-pandemic.",
                category: "Work Culture",
                tags: "Remote, Work, Tech",
                author: "workVibes",
                date: "April 4, 2025",
                image: "../assets/profile.png",
                bookmarks: 21,
                shares: 6,
                saves: 12,
                upvotes: 170,
                downvotes: 3,
                views: 1450,
                comments: 18
            },
            {
                title: "Best Resources to Learn Machine Learning",
                description: "Top courses, books, and tools to master ML from scratch.",
                category: "Machine Learning",
                tags: "ML, Learning, Resources",
                author: "mlNerd",
                date: "April 3, 2025",
                image: "../assets/profile.png",
                bookmarks: 25,
                shares: 10,
                saves: 18,
                upvotes: 190,
                downvotes: 2,
                views: 1600,
                comments: 21
            },
            {
                title: "How to Negotiate Your First Tech Salary",
                description: "Tips from devs who've been there and done that.",
                category: "Career",
                tags: "Salary, Jobs, Tech",
                author: "salaryTalk",
                date: "April 2, 2025",
                image: "../assets/profile.png",
                bookmarks: 15,
                shares: 4,
                saves: 10,
                upvotes: 140,
                downvotes: 2,
                views: 1100,
                comments: 12
            }
        ]
    },
    {
        name: "Mixed Picks",
        id: "mixed-picks-posts",
        posts: [
            {
                title: "How to Design Accessible Websites",
                description: "Ensure your site is usable by everyone, including those with disabilities.",
                category: "Accessibility",
                tags: "A11y, WCAG, Web Dev",
                author: "inclusiveDev",
                date: "April 6, 2025",
                image: "../assets/profile.png",
                bookmarks: 11,
                shares: 5,
                saves: 9,
                upvotes: 130,
                downvotes: 1,
                views: 900,
                comments: 9
            },
            {
                title: "Basics of GraphQL for Beginners",
                description: "Understand how GraphQL differs from REST and how to get started.",
                category: "APIs",
                tags: "GraphQL, API, Web Dev",
                author: "queryKing",
                date: "April 5, 2025",
                image: "../assets/profile.png",
                bookmarks: 14,
                shares: 6,
                saves: 10,
                upvotes: 145,
                downvotes: 2,
                views: 950,
                comments: 10
            },
            {
                title: "Next.js vs. Nuxt.js in 2025",
                description: "Battle of the SSR frameworks—React vs Vue showdown.",
                category: "Frameworks",
                tags: "Next.js, Nuxt.js, SSR",
                author: "metaCoder",
                date: "April 4, 2025",
                image: "../assets/profile.png",
                bookmarks: 13,
                shares: 4,
                saves: 11,
                upvotes: 150,
                downvotes: 1,
                views: 1000,
                comments: 12
            }
        ]
    }
];

categoryData.forEach(cat => {
    createCategorySection(cat.name, cat.id);
    cat.posts.forEach(post => {
        addPostToCategory(cat.id, post);
    });
});

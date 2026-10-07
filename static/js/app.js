async function api(
    url,
    options = {}
) {
    const response = await fetch(
        url,
        {
            credentials: "same-origin",
            ...options
        }
    );

    let data = {};

    try {
        data = await response.json();
    } catch (_) {
        data = {};
    }

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Request failed."
        );
    }

    return data;
}


function setMessage(
    message,
    error = false
) {
    const element =
        document.getElementById(
            "message"
        );

    if (!element) {
        return;
    }

    element.textContent =
        message || "";

    element.style.color =
        error
            ? "#c92a2a"
            : "#087f5b";
}


function escapeHtml(
    value
) {
    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        character => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        })[character]
    );
}


async function refreshNav() {

    const loginLink =
        document.getElementById(
            "loginLink"
        );

    const logoutButton =
        document.getElementById(
            "logoutBtn"
        );

    try {

        await api(
            "/api/auth/me"
        );

        if (loginLink) {
            loginLink.classList.add(
                "hidden"
            );
        }

        if (logoutButton) {
            logoutButton.classList.remove(
                "hidden"
            );
        }

    } catch (_) {
        // User is not logged in.
    }


    if (logoutButton) {

        logoutButton.onclick =
            async () => {

                await api(
                    "/api/auth/logout",
                    {
                        method: "POST"
                    }
                );

                window.location.href =
                    "/";
            };
    }
}


async function requireAuth() {

    try {

        const result =
            await api(
                "/api/auth/me"
            );

        return result.user;

    } catch (_) {

        window.location.href =
            "/login";

        return null;
    }
}


function renderResult(
    data,
    target
) {

    if (
        !data
        || typeof data !== "object"
        || Array.isArray(data)
    ) {
        throw new Error(
            "The planner returned an invalid result. Please try again."
        );
    }

    const allocationItems =
        Array.isArray(data.allocation)
            ? data.allocation
            : [];

    const recommendationItems =
        Array.isArray(data.recommendations)
            ? data.recommendations
            : [];

    const allocations =
        allocationItems
            .map(
                allocation => `
                    <div>
                        <strong>
                            ${escapeHtml(
                                allocation.category
                            )}
                        </strong>

                        <br>

                        ₹${Number(
                            allocation.amount || 0
                        ).toLocaleString(
                            "en-IN"
                        )}
                    </div>
                `
            )
            .join("");


    const recommendations =
        recommendationItems
            .map(
                item => `
                    <article
                        class="recommendation"
                    >

                        <div
                            class="recommendation-top"
                        >

                            <strong>
                                ${escapeHtml(
                                    item.name
                                )}
                            </strong>

                            <span
                                class="price"
                            >
                                ₹${Number(
                                    item.price || 0
                                ).toLocaleString(
                                    "en-IN"
                                )}
                            </span>

                        </div>


                        <div class="small">

                            ${escapeHtml(
                                item.provider
                            )}

                            · match

                            ${Math.round(
                                (
                                    Number(
                                        item.match_score
                                    ) || 0
                                ) * 100
                            )}%

                        </div>


                        <p>
                            ${escapeHtml(
                                item.description
                            )}
                        </p>


                        <a
                            href="${escapeHtml(
                                item.url
                            )}"
                            target="_blank"
                            rel="noopener"
                        >
                            Provider Site →
                        </a>

                    </article>
                `
            )
            .join("");


    target.innerHTML = `

        <span class="eyebrow">

            ${escapeHtml(
                data.source_mode || "AI"
            )}

        </span>


        <h2>
            ${escapeHtml(
                data.title
            )}
        </h2>


        <div class="summary">

            ${escapeHtml(
                data.summary
            )}

        </div>


        ${
            allocations
                ? `
                    <h3>
                        Budget Allocation
                    </h3>

                    <div class="allocation">
                        ${allocations}
                    </div>
                `
                : ""
        }


        ${
            data.per_guest_food_budget
                ? `
                    <p>

                        <strong>
                            Indicative food budget
                            per guest:
                        </strong>

                        ₹${Number(
                            data.per_guest_food_budget
                        ).toLocaleString(
                            "en-IN"
                        )}

                    </p>
                `
                : ""
        }


        ${
            data.image_analyzed
                ? `
                    <p class="small">

                        Outfit image was analyzed
                        for broad styling cues.

                    </p>
                `
                : ""
        }


        <h3>
            Recommendations
        </h3>


        <div class="recommendations">

            ${
                recommendations ||
                "<p>No recommendations returned.</p>"
            }

        </div>

    `;
}


function bindHomeForm() {

    const form =
        document.getElementById(
            "homeForm"
        );

    if (!form) {
        return;
    }


    form.onsubmit =
        async event => {

            event.preventDefault();

            setMessage(
                "Generating..."
            );


            const formData =
                new FormData(form);


            const rooms =
                [
                    ...document.querySelectorAll(
                        'input[name="rooms"]:checked'
                    )
                ].map(
                    input => input.value
                );


            try {

                const result =
                    await api(
                        "/api/generate-home",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                budget: Number(
                                    formData.get(
                                        "budget"
                                    )
                                ),

                                style:
                                    formData.get(
                                        "style"
                                    ),

                                rooms,

                                quantities: {}
                            })
                        }
                    );


                renderResult(
                    result,
                    document.getElementById(
                        "result"
                    )
                );


                setMessage(
                    "Plan generated."
                );

            } catch (error) {

                setMessage(
                    error.message,
                    true
                );
            }
        };
}


function bindPartyForm() {

    const form =
        document.getElementById(
            "partyForm"
        );

    if (!form) {
        return;
    }


    form.onsubmit =
        async event => {

            event.preventDefault();

            setMessage(
                "Generating..."
            );


            const formData =
                new FormData(form);


            try {

                const result =
                    await api(
                        "/api/generate-party",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                budget:
                                    Number(
                                        formData.get(
                                            "budget"
                                        )
                                    ),

                                guests:
                                    Number(
                                        formData.get(
                                            "guests"
                                        )
                                    ),

                                event_type:
                                    formData.get(
                                        "event_type"
                                    ),

                                venue_preference:
                                    formData.get(
                                        "venue_preference"
                                    ),

                                city:
                                    formData.get(
                                        "city"
                                    )

                            })
                        }
                    );


                renderResult(
                    result,
                    document.getElementById(
                        "result"
                    )
                );


                setMessage(
                    "Plan generated."
                );

            } catch (error) {

                setMessage(
                    error.message,
                    true
                );
            }
        };
}


function bindJewelryForm() {

    const form =
        document.getElementById(
            "jewelryForm"
        );

    if (!form) {
        return;
    }


    form.onsubmit =
        async event => {

            event.preventDefault();

            setMessage(
                "Analyzing..."
            );


            const formData =
                new FormData(form);


            try {

                const result =
                    await api(
                        "/api/generate-jewelry",
                        {
                            method: "POST",

                            body: formData
                        }
                    );


                renderResult(
                    result,
                    document.getElementById(
                        "result"
                    )
                );


                setMessage(
                    "Recommendations generated."
                );

            } catch (error) {

                setMessage(
                    error.message,
                    true
                );
            }
        };
}


function bindLoginForm() {

    const form =
        document.getElementById(
            "loginForm"
        );

    if (!form) {
        return;
    }


    form.onsubmit =
        async event => {

            event.preventDefault();

            setMessage(
                "Signing in..."
            );


            const formData =
                new FormData(form);


            try {

                await api(
                    "/api/auth/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email:
                                formData.get(
                                    "email"
                                ),

                            password:
                                formData.get(
                                    "password"
                                )

                        })
                    }
                );


                window.location.href =
                    "/dashboard";

            } catch (error) {

                setMessage(
                    error.message,
                    true
                );
            }
        };
}


function bindRegisterForm() {

    const form =
        document.getElementById(
            "registerForm"
        );

    if (!form) {
        return;
    }


    form.onsubmit =
        async event => {

            event.preventDefault();

            setMessage(
                "Creating account..."
            );


            const formData =
                new FormData(form);


            try {

                await api(
                    "/api/auth/register",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name:
                                formData.get(
                                    "name"
                                ),

                            email:
                                formData.get(
                                    "email"
                                ),

                            password:
                                formData.get(
                                    "password"
                                )

                        })
                    }
                );


                window.location.href =
                    "/login";

            } catch (error) {

                setMessage(
                    error.message,
                    true
                );
            }
        };
}


async function loadDashboard() {

    const user =
        await requireAuth();

    if (!user) {
        return;
    }


    document.getElementById(
        "welcome"
    ).textContent =
        `Welcome, ${user.name}`;


    const data =
        await api(
            "/api/history"
        );


    const target =
        document.getElementById(
            "recentHistory"
        );


    target.innerHTML =
        data.items
            .slice(0, 5)
            .map(
                item => `
                    <div
                        class="history-row"
                    >

                        <span>

                            <strong>
                                ${escapeHtml(
                                    item.planner
                                )}
                            </strong>

                            ·

                            ₹${Number(
                                item.budget
                            ).toLocaleString(
                                "en-IN"
                            )}

                            <br>

                            <span
                                class="small"
                            >
                                ${escapeHtml(
                                    item.created_at
                                )}
                            </span>

                        </span>


                        <a
                            href="/history"
                        >
                            View History
                        </a>

                    </div>
                `
            )
            .join("")
        ||
        "<p>No plans yet.</p>";
}


async function loadHistory() {

    const user =
        await requireAuth();

    if (!user) {
        return;
    }


    try {

        const data =
            await api(
                "/api/history"
            );


        const target =
            document.getElementById(
                "historyList"
            );


        target.innerHTML =
            data.items
                .map(
                    item => `
                        <div
                            class="history-row"
                        >

                            <span>

                                <strong>
                                    ${escapeHtml(
                                        item.planner
                                    )}
                                </strong>

                                ·

                                ₹${Number(
                                    item.budget
                                ).toLocaleString(
                                    "en-IN"
                                )}

                                <br>

                                <span
                                    class="small"
                                >
                                    ${escapeHtml(
                                        item.created_at
                                    )}
                                </span>

                            </span>


                            <span>

                                <button
                                    class="btn secondary"
                                    onclick="viewHistory(${item.id})"
                                >
                                    View
                                </button>


                                <button
                                    class="btn"
                                    onclick="deleteHistory(${item.id})"
                                >
                                    Delete
                                </button>

                            </span>

                        </div>
                    `
                )
                .join("")
            ||
            "<p>No saved recommendations.</p>";

    } catch (error) {

        document.getElementById(
            "historyList"
        ).textContent =
            error.message;
    }
}


async function viewHistory(
    id
) {

    const data =
        await api(
            `/api/history/${id}`
        );


    const popup =
        window.open(
            "",
            "_blank",
            "width=900,height=700"
        );


    popup.document.write(
        `
            <pre
                style="
                    white-space:pre-wrap;
                    font:16px system-ui;
                    padding:30px;
                "
            >
                ${escapeHtml(
                    JSON.stringify(
                        data.response,
                        null,
                        2
                    )
                )}
            </pre>
        `
    );
}


async function deleteHistory(
    id
) {

    if (
        !confirm(
            "Delete this history item?"
        )
    ) {
        return;
    }


    await api(
        `/api/history/${id}`,
        {
            method: "DELETE"
        }
    );


    loadHistory();
}


refreshNav();

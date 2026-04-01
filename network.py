# homepage.py
import streamlit as st
import base64

from auth import (
    add_connection,
    list_connections,
    delete_connection,  
    get_user_email,
    update_user_email,
    save_resume_pdf,
    get_resume_pdf_path,
    delete_resume_pdf,
)


def _logout():
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.view = "login"
    st.rerun()


def _ai_followup_email(name: str, company: str, notes: str, tone: str) -> str:
    greeting = f"Hi {name}," if name else "Hi there,"

    sender = st.session_state.get("user_name", "")
    if tone == "Warm":
        closing = f"Best,\n{sender}"
    elif tone == "Formal":
        closing = f"Sincerely,\n{sender}"
    else:
        closing = f"Thanks,\n{sender}"

    company_part = f" at {company}" if company else ""
    notes_part = (
        f" I really enjoyed our conversation about {notes}."
        if notes
        else " I really enjoyed our conversation."
    )

    return (
        f"{greeting}\n\n"
        f"It was great meeting you{company_part} recently.{notes_part}\n\n"
        "I’m currently exploring opportunities and would love to stay in touch. "
        "If you’re open to it, could we set up a quick 10–15 minute chat sometime next week?\n\n"
        f"{closing}"
    )


def render_homepage():
    # ---------- Protect page ----------
    if not st.session_state.get("logged_in", False):
        st.warning("Please log in first.")
        st.stop()

    # ---------- Minimal clean CSS ----------
    st.markdown(
        """
    <style>
    .block-container { max-width: 950px; padding-top: 2rem; padding-bottom: 2rem; }

    .card {
      border: 1px solid rgba(0,0,0,0.06);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 10px;
      background: #ffffff;
    }

    .muted { color: #777; font-size: 0.9rem; }

    .stTextInput input, .stTextArea textarea {
      border-radius: 8px !important;
      border: 1px solid #e6e6e6 !important;
    }

    .stButton>button {
      border-radius: 8px;
      border: 1px solid #e6e6e6;
      background: white;
      padding: 0.55rem 0.9rem;
    }
    .stButton>button:hover { border-color: #bbb; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Make sure email is populated
    if not st.session_state.get("user_email"):
        st.session_state.user_email = get_user_email(st.session_state.user_name) or ""

    # ---------- Sidebar ----------
    st.sidebar.markdown("## Network Manager")
    st.sidebar.markdown('<div class="muted">Your personal networking hub</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Connections", "AI Email Helper", "Profile", "Logout"],
    )

    # ---------- DASHBOARD ----------
    if page == "Dashboard":
        st.title("Dashboard")
        st.markdown(
            f'<div class="muted">Welcome back, <b>{st.session_state.user_name}</b>.</div>',
            unsafe_allow_html=True,
        )

        connections = list_connections(st.session_state.user_name)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total connections", len(connections))
        c2.metric("New this week", len(connections))  # placeholder
        c3.metric("Follow-ups due", 0)               # placeholder

        st.markdown("### Recent connections")
        if not connections:
            st.info("No connections yet. Add your first one in Connections.")
        else:
            for c in connections[:5]:
                st.markdown(
                    f"""
                    <div class="card">
                      <div style="font-size:1.02rem;"><b>{c['name']}</b></div>
                      <div class="muted">{c.get('company','')} • {c.get('email','')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ---------- CONNECTIONS ----------
    elif page == "Connections":
        st.title("Connections")

        left, right = st.columns([1, 1])

        with left:
            st.subheader("Add a connection")
            with st.form("add_connection_form", clear_on_submit=True):
                name = st.text_input("Name*")
                email = st.text_input("Email")
                company = st.text_input("Company")
                notes = st.text_area("Notes (where you met / what you discussed)")
                submitted = st.form_submit_button("Add Connection")

            if submitted:
                ok, msg = add_connection(
                    st.session_state.user_name,
                    name.strip(),
                    email.strip(),
                    company.strip(),
                    notes.strip(),
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with right:
            st.subheader("Your connections")
            connections = list_connections(st.session_state.user_name)

            if not connections:
                st.info("No connections yet.")
            else:
                query = st.text_input("Search", placeholder="Search by name, company, or email")
                q = query.strip().lower()

                if q:
                    filtered = []
                    for c in connections:
                        hay = f"{c.get('name','')} {c.get('company','')} {c.get('email','')}".lower()
                        if q in hay:
                            filtered.append(c)
                else:
                    filtered = connections

                st.caption(f"Showing {len(filtered)} of {len(connections)}")

                for c in filtered:
                    st.markdown(
                        f"""
                        <div class="card">
                          <div style="font-size:1.02rem;"><b>{c['name']}</b></div>
                          <div class="muted">{c.get('company','')} • {c.get('email','')}</div>
                          <div style="margin-top:8px;">{c.get('notes','')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Wider delete column so it doesn't wrap
                    col_a, col_b = st.columns([6, 2])
                    with col_b:
                        if st.button("🗑 Delete", key=f"del_{c['id']}"):
                            ok, msg = delete_connection(c["id"], st.session_state.user_name)
                            if ok:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)   
    # ---------- AI EMAIL HELPER ----------
    elif page == "AI Email Helper":
        st.title("AI Email Helper")
        st.markdown('<div class="muted">Generate a professional follow-up email in seconds.</div>', unsafe_allow_html=True)
        st.markdown("---")

        connections = list_connections(st.session_state.user_name)
        if not connections:
            st.info("Add at least one connection first.")
            st.stop()

        options = [f"{c['name']} — {c.get('company','')}".strip(" —") for c in connections]
        choice = st.selectbox("Choose a connection", options)
        selected = connections[options.index(choice)]
        tone = st.selectbox("Tone", ["Warm", "Neutral", "Formal"])

        if st.button("Generate Follow-up Email"):
            email_text = _ai_followup_email(
                name=selected.get("name", ""),
                company=selected.get("company", ""),
                notes=selected.get("notes", ""),
                tone=tone,
            )
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.text_area("Draft email", value=email_text, height=280)
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PROFILE ----------
    elif page == "Profile":
        st.title("Profile")

        st.markdown(
            f"""
            <div class="card">
              <div><b>Username:</b> {st.session_state.user_name}</div>
              <div><b>Email:</b> {st.session_state.user_email or "(not set)"}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("Update email")
        new_email = st.text_input("New email", value=st.session_state.user_email)

        if st.button("Save Email"):
            ok, msg = update_user_email(st.session_state.user_name, new_email)
            if ok:
                st.session_state.user_email = new_email.strip()
                st.success(msg)
            else:
                st.error(msg)

        st.divider()
        st.subheader("Resume (PDF)")
        uploaded = st.file_uploader("Upload your resume", type=["pdf"])

        if uploaded is not None:
            ok, msg = save_resume_pdf(st.session_state.user_name, uploaded.getvalue())
            if ok:
                st.success(msg)
            else:
                st.error(msg)

        resume_path = get_resume_pdf_path(st.session_state.user_name)
        if resume_path:
            with open(resume_path, "rb") as f:
                resume_bytes = f.read()

            st.download_button(
                label="Download current resume",
                data=resume_bytes,
                file_name="resume.pdf",
                mime="application/pdf",
            )

            st.caption("Preview (may not work in all browsers):")
            st.components.v1.iframe(
                src="data:application/pdf;base64," + base64.b64encode(resume_bytes).decode("utf-8"),
                height=500,
            )

            if st.button("Delete resume"):
                ok, msg = delete_resume_pdf(st.session_state.user_name)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.info("No resume uploaded yet.")

    # ---------- LOGOUT ----------
    elif page == "Logout":
        _logout()
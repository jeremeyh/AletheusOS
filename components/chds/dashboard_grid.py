import streamlit as st


def two_column():
    """
    Standard two-column workspace.
    """
    return st.columns([1, 1])


def three_column():
    """
    Standard three-column workspace.
    """
    return st.columns([1, 1, 1])


def sidebar_layout():
    """
    Sidebar + Content layout.
    """
    return st.columns([1, 3])


def intelligence_layout():
    """
    Intelligence Workspace layout.
    """
    return st.columns([1.2, 1, 1])


def dashboard_layout():
    """
    Four-card dashboard layout.
    """
    return st.columns(4)

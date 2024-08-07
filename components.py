import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


def input(label,value):
    html_code = f"""
                    <style>
                        .custom-input {{
                            background-color: #F0F2F6;
                            color: #62666D;
                            font-size: 13px;
                            padding: 8px;
                            border: 1px solid #F0F2F6;
                            border-radius: 8px;
                            width: 100%;
                            box-sizing: border-box;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
                        }}
                        .custom-label {{
                            font-size: 15px;
                            color: #62666D;
                            display: block;
                            margin-bottom: 4px;
                        }}
                    </style>
                    <div>
                        <label class="custom-label">{label}</label>
                        <input type="text" value="{value}" disabled class="custom-input"/>
                    </div>
                """
    return html_code
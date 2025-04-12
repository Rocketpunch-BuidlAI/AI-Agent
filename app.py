import streamlit as st
import requests

st.set_page_config(page_title="자기소개서 생성기", layout="wide")

st.title("자기소개서 생성기")

# 입력 폼 생성
with st.form("cover_letter_form"):
    # 기본 정보 입력
    st.header("Basic Information (기본 정보)")
    self_intro = st.text_area("Self Introduction (자기소개)", height=150)
    motivation = st.text_area("Motivation (지원 동기)", height=150)
    experience = st.text_area("Relevant Experience (관련 경험)", height=150)
    aspirations = st.text_area("Future Aspirations (향후 포부)", height=150)

    # 메타데이터 입력
    st.header("Metadata")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        target_company = st.text_input("Target Company (목표 회사) - 선택사항")
    with col2:
        department = st.text_input("Department (부서) - 선택사항")
    with col3:
        position = st.text_input("Position (직무) - 선택사항")
    with col4:
        position = st.text_input("Experience (경력) - 선택사항")
    with col5:
        skills = st.text_input("Skills (기술) - 선택사항")

    # 커스텀 프롬프트 입력
    st.header("Additional Settings")
    custom_prompt = st.text_area("Custom Prompt (커스텀 프롬프트) - 선택사항", height=100)

    # 제출 버튼
    submit_button = st.form_submit_button("자기소개서 생성")

if submit_button:
    # API 요청 데이터 구성
    request_data = {
        "selfIntroduction": self_intro,
        "motivation": motivation,
        "relevantExperience": experience,
        "futureAspirations": aspirations,
        "metadata": {
            "targetCompany": target_company,
            "department": department,
            "position": position,
            "experience": experience,
            "skills": skills,
        },
        "customPrompt": custom_prompt
    }

    try:
        # API 호출
        response = requests.post(
            "http://localhost:3000/edit",
            json=request_data
        )
        
        if response.status_code == 200:
            result = response.json()
            st.success("자기소개서가 생성되었습니다!")
            
            print(result)
            
            # 결과 표시
            st.header("생성된 자기소개서")
            st.write(result["text"])
            
            # 참조된 자기소개서 표시
            if result.get("sources"):
                st.header("참조된 자기소개서")
                for source in result["sources"]:
                    st.write(f"- ID: {source['id']}, Contribution: {source['contributions']} (기여도)")
        else:
            st.error(f"An error occurred: {response.text} (에러가 발생했습니다: {response.text})")
            
    except Exception as e:
        st.error(f"Error during API call: {str(e)} (API 호출 중 오류가 발생했습니다: {str(e)})")
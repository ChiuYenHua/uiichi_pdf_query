import streamlit as st
import csv
import ast
from streamlit_find_similarity_from_pinecone import get_similarity_from_pinecone

# Setup
## Control text area size
custom_css = '''
    <style>
        div.css-1om1ktf.e1y61itm0 {
          width: 800px;
        }
    </style>
    '''
st.markdown(custom_css, unsafe_allow_html=True)

## Manage state (Initialization)
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = None
if 'search_query' not in st.session_state:
    st.session_state['search_query'] = None

if 'ncku_show_how_many_results' not in st.session_state:
    st.session_state['ncku_show_how_many_results'] = 3
if 'japan_show_how_many_results' not in st.session_state:
    st.session_state['japan_show_how_many_results'] = 3
if 'china_show_how_many_results' not in st.session_state:
    st.session_state['china_show_how_many_results'] = 3
if 'taipei_show_how_many_results' not in st.session_state:
    st.session_state['taipei_show_how_many_results'] = 3

# Switch between (search) and (history)
see_history = st.toggle("查看歷史")

# In search mode
if not see_history:
    # Get input text 
    if st.session_state['search_query'] != None:
        input_text = st.text_input("關鍵句子", f"{st.session_state['search_query']}")
    else:
        input_text = st.text_input("關鍵句子", "")

    # After hit button
    if st.button("收尋pdf相關的"):
        with st.spinner('收尋中...'):
            # Get similarity data from pinecone
            data = get_similarity_from_pinecone(input_text)
            
            # Save results to session state
            st.session_state['search_results'] = data
            st.session_state['search_query'] = input_text

            # Reset session (show results)
            st.session_state['ncku_show_how_many_results'] = 3
            st.session_state['japan_show_how_many_results'] = 3
            st.session_state['china_show_how_many_results'] = 3
            st.session_state['taipei_show_how_many_results'] = 3
        
            # Store data to history
            try:
                with open(r'query_history.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([input_text, data])
            except:
                print('csv file maybe not exist!!')

    # Check if search results are already in session state
    if st.session_state['search_results'] != None:
        data = st.session_state['search_results']

        # Show all info (ncku) #################################################################
        st.header("銀髮友善住宅設計原則之研究（成大）")
        for index in range(st.session_state['ncku_show_how_many_results']):
            match = data['ncku'][index]
            st.text_area(
                f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
                match['content'],
                height=300
            )
        # Button to show more or less results
        col1, col2 = st.columns(2)
        with col1:
            if st.button('ncku_多一個結果') and st.session_state['ncku_show_how_many_results']<10:
                st.session_state['ncku_show_how_many_results'] += 1
        with col2:
            if st.button('ncku_少一個結果') and st.session_state['ncku_show_how_many_results']>1:
                st.session_state['ncku_show_how_many_results'] -= 1   
        

        # Show all info (japan) #################################################################
        st.header("日本高齡者居住的住宅設計指南（日本）")
        for index in range(st.session_state['japan_show_how_many_results']):
            match = data['japan'][index]
            st.text_area(
                f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
                match['content'],
                height=300
            )
        # Button to show more or less results
        col1, col2 = st.columns(2)
        with col1:
            if st.button('japan_多一個結果') and st.session_state['japan_show_how_many_results']<10:
                st.session_state['japan_show_how_many_results'] += 1
        with col2:
            if st.button('japan_少一個結果') and st.session_state['japan_show_how_many_results']>1:
                st.session_state['japan_show_how_many_results'] -= 1   


        # Show all info (china) #################################################################
        st.header("老年人居住建築設計規範（中國）")
        for index in range(st.session_state['china_show_how_many_results']):
            match = data['china'][index]
            st.text_area(
                f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
                match['content'],
                height=300
            )
        # Button to show more or less results
        col1, col2 = st.columns(2)
        with col1:
            if st.button('china_多一個結果') and st.session_state['china_show_how_many_results']<10:
                st.session_state['china_show_how_many_results'] += 1
        with col2:
            if st.button('china_少一個結果') and st.session_state['china_show_how_many_results']>1:
                st.session_state['china_show_how_many_results'] -= 1   


        # Show all info (taipei) #################################################################
        st.header("臺北市居住空間通用設計指南（臺北市）")
        for index in range(st.session_state['taipei_show_how_many_results']):
            match = data['taipei'][index]
            st.text_area(
                f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
                match['content'],
                height=300
            )
        # Button to show more or less results
        col1, col2 = st.columns(2)
        with col1:
            if st.button('taipei_多一個結果') and st.session_state['taipei_show_how_many_results']<10:
                st.session_state['taipei_show_how_many_results'] += 1
        with col2:
            if st.button('taipei_少一個結果') and st.session_state['taipei_show_how_many_results']>1:
                st.session_state['taipei_show_how_many_results'] -= 1   


# In history mode
else:
    results_list = []

    # Open the CSV file
    with open('query_history.csv', mode='r') as file:
        # Use DictReader to read the file as a dictionary
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            row['data'] = ast.literal_eval(row['data'])
            results_list.append(row)

    query_list = [i['query'] for i in results_list]
    option = st.selectbox(
        "哪個收尋的歷史資料？",
        query_list,
    )

    data = [i for i in results_list if i['query']==option][0]['data']
    
    # Show answer
    # Show all info (ncku) #################################################################
    st.header("銀髮友善住宅設計原則之研究（成大）")
    for index, match in enumerate(data['ncku']):
        st.text_area(
            f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
            match['content'],
            height=300
        )

    # Show all info (japan) #################################################################
    st.header("日本高齡者居住的住宅設計指南（日本）")
    for index, match in enumerate(data['japan']):
        st.text_area(
            f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
            match['content'],
            height=300
        )

    # Show all info (china) #################################################################
    st.header("老年人居住建築設計規範（中國）")
    for index, match in enumerate(data['china']):
        st.text_area(
            f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
            match['content'],
            height=300
        )

    # Show all info (taipei) #################################################################
    st.header("臺北市居住空間通用設計指南（臺北市）")
    for index, match in enumerate(data['taipei']):
        st.text_area(
            f"排序{index+1}, 頁數：{int(match['page'])}, 相似度：{round(match['score'], 3)}",
            match['content'],
            height=300
        )

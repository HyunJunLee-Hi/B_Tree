# B_Tree
##### B_트리의 max degree (order)는 3, 5, 7을 기준으로 구현하였습니다. 
##### 기본 max degree는 5입니다. (수정을 원하면 코드에서 7번째 줄에 있는 m 변수 값을 변경하면 됩니다.
##### ‘1’을 입력하여 insertion을 진행한 뒤 ‘2’를 입력해서 deletion을 진행해야 합니다.
## Insertion
##### ‘1’을 입력하면 위의 사진과 같이 insertion을 진행할 데이터가 있는 csv 파일 이름을 입력하게 됩니다. 
##### 이때 확장자명 .csv를 제외한 파일명만 입력하여야 합니다. (‘input’, ‘input2’를 입력해야 합니다.)
##### 파일명을 입력하면 insert가 진행됩니다. 
##### 완료가 되면 완료 메시지와 함께 실행에 걸린 시간이 출력됩니다. 
##### 또한 기존의 input.csv 파일과 input_result.csv 파일을 비교하여 일치하지 않는 결과의 개수를 출력시킵니다. 
##### 그 뒤 다시 처음 메뉴를 선택하는 화면이 나타납니다.
##### Insert 결과는 실행 파일이 있는 폴더 내부에 ‘파일명_result.csv’ 형태로 생성됩니다.
## Deletion
##### Deletion을 실행시키면 deletion을 진행할 데이터가 있는 파일 이름을 입력하게 됩니다.
##### Insertion과 마찬가지로 확장자명 .csv를 제외한 파일명만 입력하여야 합니다. (‘delete’, ‘delete2’)
##### 파일명을 입력하면 deletion이 진행됩니다. 완료가 되면 완료 메시지와 함께 실행에 걸린 시간이 출력됩니다. 그 뒤 다시 처음 메뉴를 선택하는 화면이 나타납니다.
##### Delete 결과는 실행 파일이 있는 폴더 내부에 ‘New_파일명_result.csv’ 형태로 생성됩니다.
## Delete Check
##### 삭제가 잘 되었는지 확인하는 작업을 위해 삭제 결과 원본 csv 파일을 이름을 입력하게 됩니다. 
##### 이때 역시 확장자명 .csv를 제외한 파일명만 입력하여야 합니다. (‘delete_result’, ‘delete_result2’)
##### 초기에 주어졌던 delete_result.csv, delete_result2.csv 파일과 프로그램 결과 파일인 New_delete_result.csv, New_delete_result2.csv 파일과 비교하여 일치하지 않는 데이터의 개수를 출력합니다.

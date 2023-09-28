class Constants:
    # Success
    SIGNUP_SUCCESS = "Đăng ký thành công"
    LOGIN_SUCCESS = "Đăng nhập thành công"
    ANSWER_SUCCESS = "Gửi câu trả lời thành công"
    USER_INFO = "Thông tin của bạn"
    USER_CHECKIN = "Thông tin điểm danh của bạn"
    USER_CHECKIN_SUCCESS = "Điểm danh thành công"
    USER_DAILY_QUESTIONS = "Danh sách câu hỏi hàng ngày của bạn"

    # Failure
    LOGIN_FAILED = (
        "Tên đăng nhập, mật khẩu hoặc thiết bị đăng nhập không đúng. Vui lòng thử lại!"
    )
    USER_INFO_FAILED = "Lấy thông tin của bạn thất bại"
    USERNAME_EXIST = "Tên đăng nhập đã tồn tại"
    EMAIL_EXIST = "Email đã tồn tại"
    DEVICE_EXIST = "Thiết bị đã được sử dụng để đăng ký"
    PERMISSION_DENIED = "Bạn không thể thực hiện hành động này"
    UNAUTHORIZED = "Thông tin xác thực không chính xác"
    USER_ALREADY_CHECKED_IN = "Đã điểm danh ngày hôm nay"


constants = Constants()

class Constants:
    # Success
    SIGNUP_SUCCESS = "Đăng ký thành công"
    LOGIN_SUCCESS = "Đăng nhập thành công"
    USER_INFO = "Thông tin người dùng"
    USER_CHECKIN = "Thông tin điểm danh của người dùng"
    USER_CHECKIN_SUCCESS = "Điểm danh thành công"

    # Failure
    LOGIN_FAILED = (
        "Tên đăng nhập, mật khẩu hoặc thiết bị đăng nhập không đúng. Vui lòng thử lại!"
    )
    USER_INFO_FAILED = "Lấy thông tin người dùng thất bại"
    USERNAME_EXIST = "Tên đăng nhập đã tồn tại"
    EMAIL_EXIST = "Email đã tồn tại"
    DEVICE_EXIST = "Thiết bị đã được sử dụng để đăng ký"
    PERMISSION_DENIED = "Bạn không thể thực hiện hành động này"
    UNAUTHORIZED = "Thông tin xác thực không chính xác"
    USER_ALREADY_CHECKED_IN = "Đã điểm danh ngày hôm nay"


constants = Constants()
